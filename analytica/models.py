from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


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
    password_hash = db.Column(db.String(length=60), nullable=False)
    analyzed_products_num = db.Column(db.Integer(), default=0, nullable=False)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirm_token = db.Column(db.String(60), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bycrypt.generate_password_hash(plain_text_password) 

    def check_password_correction(self, attempted_password):
       return bycrypt.check_password_hash(self.password_hash, attempted_password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
