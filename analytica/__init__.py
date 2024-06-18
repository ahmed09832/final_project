from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projrect.db'
app.config['SECRET_KEY'] = '99ede3e32af135ccb18ae609'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ahmedshawaly70@gmail.com'
app.config['MAIL_PASSWORD'] = 'c q e a j x h y r q l t j d u r'
 

db = SQLAlchemy(app)
mail = Mail(app)
bycrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from analytica import routes