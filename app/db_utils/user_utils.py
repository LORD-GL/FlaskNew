from sqlalchemy.exc import IntegrityError

def add_user(username: str, email: str, password: str):
    from app import db
    from app.models import User
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        return False