from flask import render_template, request, session, url_for, redirect
from app import app, db
from app.models import UserDB, add_user, News
from sqlalchemy import text

#redirect(url_for('dashboard'))

def save_user_session(username):
    session['logged_in'] = True
    session['username'] = username


@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        message = f"\nYou are logined by {session['username']}"
    else:
        message = "You aren't logined!"
        
    sql_getall = text('SELECT * FROM news;')
    news = db.session.execute(sql_getall)
    if news:
        return render_template('index.html', pageName="Home Page", news = news, message = message)
    else:
        return "There are any users"


@app.route('/article/<int:id>')
def article(id):
    article_i = News.query.get_or_404(int(id))
    article_i.views += 1
    db.session.commit()
    return render_template("article.html", article = article_i)


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        if add_user(request.form['username'], request.form['email'], request.form['password']):
            save_user_session(request.form['username'])
            return redirect(url_for('index'))
        else:  
            return render_template('singup.html', pageName="Sing Up", message="Username or email is already taken") 
    else:
        return render_template('singup.html', pageName="Sing Up")


@app.route('/users')
def usersGet():
    sql_getall = text('SELECT * FROM user_db;')
    users = db.session.execute(sql_getall)
    if users:
        return render_template('users.html', pageName="Users List", users=users)
    else:
        return "There are any users"
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = UserDB.query.filter_by(username=request.form['username']).first()
        if user:
            if user.check_password(request.form['password']):
                save_user_session(request.form['username'])
                return redirect(url_for('index'))
            else:
                return render_template('login.html', pageName='Login', message="Password is wrong")
        else:
            return render_template('login.html', pageName="Login", message="There is no such user")
    else:
        return render_template('login.html', pageName='Login', message="")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
