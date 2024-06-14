from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import re, requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired, ValidationError, EqualTo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projrect.db'
app.config['SECRET_KEY'] = '99ede3e32af135ccb18ae609'
db = SQLAlchemy(app)
bycrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    analyzed_products_num = db.Column(db.Integer(), default=0, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bycrypt.generate_password_hash(plain_text_password) 

    def check_password_correction(self, attempted_password):
       return bycrypt.check_password_hash(self.password_hash, attempted_password)



class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        user =  User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email Address already exists! Please try a different email address")


    username = StringField(label='UserName:', 
                           validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', 
                                validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', 
                              validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(label='Confirm Password:', 
                              validators=[EqualTo('password1', DataRequired())])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', 
                                validators=[Email(), DataRequired()]) 
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In:')


def is_valid_url_or_code(form, field):
    input_value = field.data
    url_pattern = r'^https?://(?:www\.)?amazon\.[a-z]{2,3}(?:\.[a-z]{2})?/.*[/?]dp/([A-Z0-9]{10})(?:/.*)?$'
    code_pattern = r'^[A-Z0-9]{10}$'

    if re.match(code_pattern, input_value):
        url = f"https://www.amazon.com/dp/{input_value}"
    else:
        url = input_value

    if not re.match(url_pattern, url):
        raise ValidationError('Invalid Amazon product URL or code format.')

    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            raise ValidationError('The product URL is not accessible.')
    except requests.RequestException as e:
        raise ValidationError(f'Error accessing the URL: {str(e)}')

class ProductCodeForm(FlaskForm):
    product_url_or_code = StringField('Product URL or Code', validators=[DataRequired(), is_valid_url_or_code])
    submit = SubmitField(label='Analysis')





@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = ProductCodeForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard_page'))
    return render_template('home.html', form=form)



@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)

