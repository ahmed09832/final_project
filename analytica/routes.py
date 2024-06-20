from flask import Flask, render_template, redirect, url_for, flash
from analytica.forms import ProductCodeForm, RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from analytica.models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from analytica import app, db, mail

# from analytica.utils import send_reset_email
import secrets


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
        return redirect(url_for('dashboard_page'))
                                  
    if form.errors != {}: #If there are not errors from the validations
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
    return render_template('dashboard.html')




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
    print(user.email_address, user.username)
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
