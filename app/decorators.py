from flask_login import current_user
from flask import render_template, url_for, redirect
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.username == 'root':
                return f(*args, **kwargs)
        return render_template("access_denied.html")
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function