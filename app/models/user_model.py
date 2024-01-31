from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, default="username")
    email = db.Column(db.String(100), unique=True, nullable=False, default="default@gmail.com")
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256), nullable=False, default="HASH") 
    articles = relationship('Article', back_populates='author_account')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return self.username
