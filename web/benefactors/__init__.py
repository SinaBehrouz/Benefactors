import os
import secrets
import stripe
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", secret_key)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///site.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

stripe_keys = {
  'secret_key': os.getenv("STRIPE_SECRET_KEY", "sk_test_51HAlzwJxCod5ibwzuOmzGJwQ4AjYksOWNCVqlC9fLAvU2v0WuVm6Rv6Yxf0G2oMGFSqniqZ7ElblIq243kMbcO1l00TrMS8g62"),
  'publishable_key': os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_51HAlzwJxCod5ibwz1qoTHZ6sNfXWBsKtjFwLgxsc0U5UUZmMUMmz8MsUM8ksbA8n57qVLLHlJKd4McTTh3fU4FLP00FnJrzKTr")
}

stripe.api_key = stripe_keys['secret_key']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from benefactors import routes
