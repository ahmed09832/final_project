import re, requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired, ValidationError, EqualTo
from analytica.models import User

from analytica.scraping import get_html_content_pos, extract_asin

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
                              validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address:', 
                                validators=[Email(), DataRequired()]) 
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In:')


# def is_valid_url_or_code(form, field):
#     input_value = field.data
#     url_pattern = r'^https?://(?:www\.)?amazon\.[a-z]{2,3}(?:\.[a-z]{2})?/.*[/?]dp/([A-Z0-9]{10})(?:/.*)?$'
#     code_pattern = r'^[A-Z0-9]{10}$'

#     if re.match(code_pattern, input_value):
#         url = f"https://www.amazon.com/dp/{input_value}"
#     else:
#         url = input_value

#     print("---------------------------------->\n")
#     print(not re.match(url_pattern, url))
#     print("---------------------------------->\n")

#     if not re.match(url_pattern, url):
#         print("HI ------------------- HI")
#         raise ValidationError('Invalid Amazon product URL or code format.')

#     try:
#         res = requests.get(url, timeout=10)
#         if res.status_code != 200:
#             raise ValidationError('The product URL is not accessible.')
#     except requests.RequestException as e:
#         raise ValidationError(f'Error accessing the URL: {str(e)}')


def is_valid_url_or_code(form, field):
    input_value = field.data
    url_pattern = r'^https?://(?:www\.)?amazon\.[a-z]{2,3}(?:\.[a-z]{2})?/.*[/?]dp/([A-Z0-9]{10})(?:/.*)?$'
    code_pattern = r'^[A-Z0-9]{10}$'
    
    

    if not re.match(code_pattern, input_value):
        product_code = extract_asin(input_value)
        
    else: 
        product_code = input_value
                
    try:
        res = get_html_content_pos(product_code, 1)
        if res.status_code != 200:
            raise ValidationError('The product URL is not accessible.')
    except requests.RequestException as e:
        raise ValidationError(f'Error accessing the URL: {str(e)}')
    
    
class ProductCodeForm(FlaskForm):
    product_url_or_code = StringField('Product URL or Code', validators=[DataRequired(), is_valid_url_or_code])
    submit = SubmitField(label='Analysis')


class RequestResetForm(FlaskForm):
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')