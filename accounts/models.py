from src.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __str__(self):
        return self.username

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
