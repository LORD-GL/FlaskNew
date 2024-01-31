from app import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'article'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Title")
    image = db.Column(db.String(150), default="/static/images/default_image.jpg")
    description = db.Column(db.String(500), nullable=False, default="Description")
    content = db.Column(db.Text, nullable=False, default="Content")
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    # reactions = db.Column(db.JSON, default={
    #     'likes' : [], 'cry' : [], 'funny' : []
    # })
    author = db.Column(db.String(100), nullable=False, default="Author")
    author_account_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_account = relationship('User', back_populates='articles')
    themes = relationship('Theme', secondary='article_theme_association', back_populates='articles')

    def __repr__(self) -> str:
        return self.title