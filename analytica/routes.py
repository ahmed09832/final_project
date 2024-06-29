from flask import Flask, render_template, redirect, url_for, flash
from analytica.forms import ProductCodeForm, RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from analytica.models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from analytica import app, db, mail
from analytica.scraping import get_reviews
from analytica.predictions import get_sentiments, get_top_text_bysize
# from analytica.utils import send_reset_email
import secrets
import numpy as np
import plotly.express as px



# Define the variables globally
pie_fig = None
bar_fig_left = None
bar_fig_right = None
pos_reviews = None
neg_reviews = None



def generate_plots_and_wordclouds(sentiments):
    global pie_fig, bar_fig_left, bar_fig_right, pos_reviews, neg_reviews
    
    # Extract positive and negative reviews
    pos_reviews = [review for review, sentiment in sentiments if sentiment == 1]
    neg_reviews = [review for review, sentiment in sentiments if sentiment == 0]
    
    # Data for the pie chart
    labels, counts = np.unique([sentiment for _, sentiment in sentiments], return_counts=True)
    pie_data = dict(zip(labels, counts))

    # Customize pie chart appearance
    pie_fig = px.pie(names=pie_data.keys(), values=pie_data.values(), hole=0.3,
                     labels={'labels': 'Sentiment'},
                     color_discrete_sequence=px.colors.qualitative.Set2)

    # Data for horizontal bar charts
    top_pos_text = get_top_text_bysize(pos_reviews)
    top_neg_text = get_top_text_bysize(neg_reviews)

    bar_data_left = top_pos_text.sort_values()
    bar_data_right = top_neg_text.sort_values()
    
    # Customize horizontal bar charts appearance
    bar_fig_left = px.bar(x=bar_data_left.values, y=bar_data_left.index, orientation='h',
                          color_discrete_sequence=px.colors.qualitative.Plotly)
    bar_fig_right = px.bar(x=bar_data_right.values, y=bar_data_right.index, orientation='h',
                           color_discrete_sequence=px.colors.qualitative.Plotly)

    bar_fig_right.update_layout(
        xaxis_title='Count',
        yaxis_title='Top Negative Bigrams'
    )

    bar_fig_left.update_layout(
        xaxis_title='Count',
        yaxis_title='Top Positive Bigrams'
    )






def send_verification_email(user):
    token = user.confirm_token   
    msg = Message('Email Verification', sender='ahmedshawaly70@gmail.com', recipients=[user.email_address])
    msg.body = f'''To verify your email, visit the following link:
{url_for('verify_email', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ahmedshawaly70@gmail.com', recipients=[user.email_address])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = ProductCodeForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if current_user.analyzed_products_num < 100:
                current_user.analyzed_products_num += 1
                db.session.commit()

                reviews = get_reviews(form.product_url_or_code.data)


                sentiments = get_sentiments(reviews)
                print(sentiments)

                global pie_fig, bar_fig_left, bar_fig_right
                if pie_fig is None or bar_fig_left is None or bar_fig_right is None:
                    generate_plots_and_wordclouds(sentiments)


                return redirect(url_for('dashboard_page'))
            else:
                flash('You have reached the limit of analyzed products.', category='danger')
        else:
            return redirect(url_for('login_page'))

    if form.errors != {}: # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Incorrect URL or ID: {err_msg}', category='danger')

    return render_template('home.html', form=form)





@app.route("/about")
def about_page():
    return render_template("about.html")




@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data, 
                              confirm_token=secrets.token_urlsafe(16))
        db.session.add(user_to_create)
        db.session.commit()

        send_verification_email(user_to_create)
        flash('An email has been sent with instructions to verify your email.', 'info')
        return redirect(url_for('login_page'))

        # login_user(user_to_create)
        # flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        # return redirect(url_for('home_page'))


    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            if attempted_user.confirmed:
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('Please verify your email before logging in.', 'warning')

        else:
            flash('Email Address and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route("/verify_email/<token>")
def verify_email(token):
    user = User.query.filter_by(confirm_token=token).first_or_404()
    if user:
        user.confirmed = True
        user.confirm_token = None
        db.session.commit()
        flash('Your account has been verified!', 'success')
        return redirect(url_for('login_page'))
    else:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('register_page'))



@app.route('/dashboard')
@login_required
def dashboard_page():
    
    pos_summary, neg_summary = 'this is pos', 'this is neg'

    return render_template('dashboard.html', pie_html=pie_fig.to_html(full_html=False),
                        bar_left_html=bar_fig_left.to_html(full_html=False),
                        bar_right_html=bar_fig_right.to_html(full_html=False),
                        pos_summary=pos_summary, neg_summary=neg_summary)





@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login_page'))
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login_page'))
    return render_template('reset_token.html', form=form)
