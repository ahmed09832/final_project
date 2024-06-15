from flask import Flask, render_template, redirect, url_for, flash
from analytica.forms import ProductCodeForm, RegisterForm, LoginForm
from analytica.models import User

from analytica import app



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


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
