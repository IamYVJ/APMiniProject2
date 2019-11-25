from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view ='login'


app.config.update(dict(
    MAIL_SERVER="smtp.googlemail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=1,
    MAIL_USERNAME="systems.quadcore@gmail.com",
    MAIL_PASSWORD="Quadcore00",
    ADMINS = ["systems.quadcore@gmail.com"]
))


mail = Mail(app)

from app import routes, models
