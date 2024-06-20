from flask_mail import Message
from analytica import mail
from flask import url_for

def send_verification_email(user):
    token = user.confirm_token
    msg = Message('Email Verification', sender='ahmedshawaly70@gmail.com', recipients=[user.email_address])
    msg.body = f'''To verify your email, visit the following link:
{url_for('verify_email', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ahmedshawaly70@gmail.com', recipients=[user.email_address])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)
