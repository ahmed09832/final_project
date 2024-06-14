from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projrect.db'
app.config['SECRET_KEY'] = '99ede3e32af135ccb18ae609'
db = SQLAlchemy(app)
bycrypt = Bcrypt(app)


from analytica import routes
