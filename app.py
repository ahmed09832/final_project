from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


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

    





@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")



if __name__ == '__main__':
    app.run(debug=True)

