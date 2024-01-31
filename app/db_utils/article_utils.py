from sqlalchemy.exc import IntegrityError

def add_article(title: str, description: str, content: str, author: str, author_account):
    from app.models import Article
    from app import db 
    try:
        new_article = Article(title=title, description=description, content=content, author=author, author_account=author_account)
        db.session.add(new_article)
        db.session.commit()
        return new_article
    except IntegrityError:
        db.session.rollback()
        return False