from flask import Blueprint
from app.db_utils import add_user
from app.decorators import admin_required, login_required
from flask_login import login_user, logout_user
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from flask import render_template, request, url_for, redirect, session
from app.forms import LoginForm, SingUpForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/<username>')
def user(username):
    from app.models import User
    cur_user = User.query.filter_by(username=username).first()
    if cur_user:
        return render_template('auth/user.html', user=cur_user, pageName="Portfolio")
    else:
        return render_template("errors/404.html", pageName="Error")


@user_bp.route('/singup', methods=['GET', 'POST'])
def singup():
    form = SingUpForm()
    message = ""
    if form.validate_on_submit():
        new_user = add_user(form.username.data, form.email.data, str(form.password.data))
        if new_user is not False:
            login_user(new_user)
            return redirect(url_for('main.index'))
        else:
            message = "Username or email is already taken."
            return render_template('auth/singup.html', form=form, pageName="Sing Up", message=message)
    return render_template('auth/singup.html', form=form, pageName="Sing up", message=message)


@user_bp.route('/users')
@admin_required
def usersGet():
    from app import db
    try:
        sql_getall = text('SELECT * FROM user;')
        users = db.session.execute(sql_getall)
        return render_template('admin/users.html', pageName="Users List", users=users)
    except ProgrammingError:
        return "There are any users"


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app.models import User
    form = LoginForm()
    if form.validate_on_submit():
        cur_user = User.query.filter_by(username=form.username.data).first()
        if cur_user:
            if cur_user.check_password(str(form.password.data)):
                login_user(cur_user)
                return redirect(url_for('main.index'))
            else:
                return render_template('auth/login.html', form=form, pageName='Login', message="Password is wrong")
        else:
            return render_template('auth/login.html', form=form,  pageName="Login", message="There is no such user")
    return render_template('auth/login.html', form=form,  pageName="Login", message="")


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session['viewed_articles'] = []
    return redirect(url_for('main.index'))