from email.policy import default
from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

###################################################################

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
    

def add_user(username: str, email: str, password: str):
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        return False
    
###################################################################
    
class Article(db.Model):
    __tablename__ = 'article'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Title")
    image = db.Column(db.String(150), default="/static/images/default_image.jpg")
    description = db.Column(db.String(500), nullable=False, default="Description")
    content = db.Column(db.Text, nullable=False, default="Content")
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    reactions = db.Column(db.JSON, default={
        'likes' : [], 'cry' : [], 'funny' : []
    })
    author = db.Column(db.String(100), nullable=False, default="Author")
    author_account_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_account = relationship('User', back_populates='articles')
    themes = relationship('Theme', secondary='article_theme_association', back_populates='articles')

    def __repr__(self) -> str:
        return self.title
    

def add_article(title: str, description: str, content: str, author: str, author_account: User):
    try:
        new_article = Article(title=title, description=description, content=content, author=author, author_account=author_account)
        db.session.add(new_article)
        db.session.commit()
        return new_article
    except IntegrityError:
        db.session.rollback()
        return False
    
    
###################################################################
    
class Theme(db.Model):
    __tablename__ = 'theme'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(110), nullable=False)
    articles = relationship('Article', secondary='article_theme_association', back_populates='themes')


article_theme_association = db.Table(
    'article_theme_association',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')) ,
    db.Column('theme_id', db.Integer, db.ForeignKey('theme.id'))
)
