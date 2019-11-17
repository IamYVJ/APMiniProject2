from datetime import datetime
from app import app, db , login_manager, bcrypt
from flask_login import UserMixin
from time import time
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # name= db.Column(db.String(120))
    # address1= db.Column(db.String(120))
    # address2= db.Column(db.String(120))
    # city= db.Column(db.String(120))
    # state= db.Column(db.String(120))
    # zipcode= db.Column(db.Integer())
    # tokens = db.Column(db.Text)
    # type=db.Column(db.Text)

    # posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def set_password(self, password):
        self.password =  bcrypt.generate_password_hash(password).decode('utf-8')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)