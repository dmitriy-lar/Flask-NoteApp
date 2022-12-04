from flask import Flask
from dotenv import load_dotenv
from accounts.routes import accounts
from notes.routes import notes
from .extensions import db
from flask_login import LoginManager
from accounts.models import UserModel
from notes.models import Note
import os

load_dotenv()
app = Flask(__name__)
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(notes, url_prefix='/notes')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'accounts.signin_user'
login_manager.login_message = 'Пожалуйста войдите в аккаунт'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return UserModel.query.get(int(user))
