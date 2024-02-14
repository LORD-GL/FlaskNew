from flask import Blueprint
from app.db_utils import add_user
from app.decorators import admin_required, login_required
from flask_login import login_user, logout_user
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from flask import render_template, request, url_for, redirect, session

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<username>')
def user(username):
    from app.models import User
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('auth/user.html', user=user, pageName="Portfolio")
    else:
        return render_template("errors/404.html", pageName="Error")


@user_bp.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return render_template('auth/singup.html', pageName="SingUp", message="Passwords must match")
        new_user = add_user(request.form['username'], request.form['email'], request.form['password'])
        if new_user is not False:
            login_user(new_user)
            return redirect(url_for('main.index'))
        else:  
            return render_template('auth/singup.html', pageName="Sing Up", message="Username or email is already taken") 
    else:
        return render_template('auth/singup.html', pageName="Sing Up")


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
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                return render_template('auth/login.html', pageName='Login', message="Password is wrong")
        else:
            return render_template('auth/login.html', pageName="Login", message="There is no such user")
    else:
        return render_template('auth/login.html', pageName='Login', message="")


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session['viewed_articles'] = []
    return redirect(url_for('main.index'))