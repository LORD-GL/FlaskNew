import os
from flask import render_template, request, url_for, redirect, flash
from app import app, db, login_manager
from app.models import UserDB, add_article, add_user, News
from sqlalchemy import text
from flask_login import login_user, current_user, login_required, logout_user
# from PIL import Image
import os

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Загрузчик пользователей
@login_manager.user_loader
def load_user(user_id):
    return UserDB.query.get(int(user_id))


# def resize_image(input_name: str, output_name: str, new_size) -> bool:
#     try:
#         image = Image.open("static/images/"+input_name)
#         resized_image = image.resize(new_size)
#         resized_image.save("static/images/"+output_name)
#         return True
#     except Exception:
#         return False


@app.route('/')
def index():
    if current_user.is_authenticated:
        message = f"\nHello {current_user.username}"
    else:
        message = "Hello anonymous!"
        
    sql_getall = text('SELECT * FROM news;')
    news = db.session.execute(sql_getall)
    if news:
        return render_template('index.html', pageName="Home Page", news = news, message = message)
    else:
        return "There are any users"


@app.route('/new/article', methods=['GET', 'POST'])
@login_required
def new_article():
    if request.method == 'POST':
        image = request.files['file']
        if allowed_file(image.filename):
            new_article = add_article(request.form['title'], request.form['description'], request.form['content'], request.form['author'])
            if new_article is False:
                return render_template('new_article.html', message="Something went wrong during creating new Article")
            else:
                image_name = str(new_article.id) + "."
                image_name += '.' in image.filename and image.filename.rsplit('.', 1)[1].lower()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
                new_article.image = "images/"+image_name
                db.session.commit()
                # flash('Article successfully uploaded')
                return redirect(url_for('article', id=new_article.id))
        else:
            return render_template('new_article.html', message="Image format isn't supporting")
    else:
        return render_template('new_article.html', message="")


@app.route('/article/<int:id>')
def article(id):
    article_i = News.query.get_or_404(int(id))
    article_i.views += 1
    db.session.commit()
    return render_template("article.html", article = article_i)


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        new_user = add_user(request.form['username'], request.form['email'], request.form['password'])
        if new_user is not False:
            login_user(new_user)
            return redirect(url_for('index'))
        else:  
            return render_template('singup.html', pageName="Sing Up", message="Username or email is already taken") 
    else:
        return render_template('singup.html', pageName="Sing Up")


@app.route('/users')
@login_required
def usersGet():
    if current_user.username == 'root':
        sql_getall = text('SELECT * FROM user_db;')
        users = db.session.execute(sql_getall)
        if users:
            return render_template('users.html', pageName="Users List", users=users)
        else:
            return "There are any users"
    else:
        return "You are not a root user!"
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = UserDB.query.filter_by(username=request.form['username']).first()
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', pageName='Login', message="Password is wrong")
        else:
            return render_template('login.html', pageName="Login", message="There is no such user")
    else:
        return render_template('login.html', pageName='Login', message="")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
