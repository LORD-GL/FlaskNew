from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UserDB(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256), nullable=False) #128

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return self.username
    

def add_user(username: str, email: str, password: str):
    try:
        new_user = UserDB(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        return False
    
#################################################################
    
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(150), default="/static/images/default_image.jpg")
    description = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    author = db.Column(db.String(70), nullable=False)

    def __repr__(self) -> str:
        return self.title
    

def add_article(title: str, description: str, content: str, author: str):
    try:
        new_article = News(title=title, description=description, content=content, author=author)
        db.session.add(new_article)
        db.session.commit()
        return new_article
    except IntegrityError:
        db.session.rollback()
        return False