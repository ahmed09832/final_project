from flask import Flask, render_template, redirect, url_for, flash
from analytica.forms import ProductCodeForm, RegisterForm, LoginForm
from analytica.models import User

from analytica import app, db



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = ProductCodeForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard_page'))
    return render_template('home.html', form=form)

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data, 
                              password_hash = form.password1.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account created successfully!', category='success')

        return redirect(url_for('home_page'))
    
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template("register.html", form=form)


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
