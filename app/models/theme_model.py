from app import db
from sqlalchemy.orm import relationship

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
