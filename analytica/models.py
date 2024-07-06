import jwt
from datetime import datetime, timedelta

from analytica import db, bycrypt, login_manager, app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=255), nullable=False)
    analyzed_products_num = db.Column(db.Integer(), default=0, nullable=False)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirm_token = db.Column(db.String(60), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bycrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
       return bycrypt.check_password_hash(self.password_hash, attempted_password)

    def get_reset_token(self, expires_sec=1800):
        payload = {
            "user_id": self.id,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Expires in 1 hour
        }

        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")


    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, 
                                 app.config['SECRET_KEY'], algorithms=["HS256"], options={"verify_exp": True})['user_id']
        except:
            return None
        return User.query.get(user_id)
