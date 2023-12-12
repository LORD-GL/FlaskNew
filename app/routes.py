import os
from flask import render_template, request, url_for, redirect, flash, session
import sqlalchemy
from app import app, db, login_manager
from app.models import User, add_article, add_user, Article
from sqlalchemy import text
from flask_login import login_user, current_user, logout_user
from app.forms import NewsForm
from functools import wraps
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return render_template("access_denied.html")
        return f(*args, **kwargs)
    return decorated_function


# from PIL import Image
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

    try: 
        sql_getall = text('SELECT * FROM article;')
        news = db.session.execute(sql_getall)
        return render_template('index.html', pageName="Home Page", news = news, message = message)
    except sqlalchemy.exc.ProgrammingError:
        return "Error"


@app.route('/new/article', methods=['GET', 'POST'])
@login_required
def new_article():
    if request.method == 'POST':
        image = request.files['file']
        if allowed_file(image.filename):
            new_article = add_article(request.form['title'], request.form['description'], request.form['content'], request.form['author'], current_user)
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


@app.route('/delete/article/<int:id>')
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    if current_user.username == "root" or current_user.id == article.author_account.id:
        db.session.delete(article)
        db.session.commit()
        flash("Article has been succesfully deleted")
        return redirect(url_for('index'))
    else:
        return render_template("access_denied.html")


@app.route('/edit/article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if current_user.username == "root" or current_user.id == article.author_account.id:
        form = NewsForm(obj=article)
        if form.validate_on_submit():
            form.populate_obj(article)
            article.title = form.title.data
            article.description = form.description.data
            article.content = form.content.data
            article.author = form.author.data
            try:
                image_name = str(article.id) + "."
                image_name += '.' in form.image.data.filename and form.image.data.filename.rsplit('.', 1)[1].lower()
                form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
                article.image = "images/"+image_name
            except AttributeError:
                pass
            else:
                render_template('edit_article.html', form=form, article=article, message="Error during saving the image")
            finally:
                db.session.commit()
                return redirect(url_for("article", id = article.id))
        return render_template('edit_article.html', form=form, article=article)
    else:
        return render_template("access_denied.html")


@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(int(id))
    viewed_articles_key = 'viewed_articles'
    if viewed_articles_key not in session:
        session[viewed_articles_key] = []
    if id not in session[viewed_articles_key]:
        article.views += 1
        db.session.commit()
        session[viewed_articles_key].append(id)
    return render_template("article.html", article = article, pageName="Article")


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user, pageName="Portfolio")


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            return render_template('singup.html', pageName="SingUp", message="Passwords must match")
        new_user = add_user(request.form['username'], request.form['email'], request.form['password'])
        if new_user is not False:
            login_user(new_user)
            return redirect(url_for('index'))
        else:  
            return render_template('singup.html', pageName="Sing Up", message="Username or email is already taken") 
    else:
        return render_template('singup.html', pageName="Sing Up")


@app.route('/users')
def usersGet():
    if current_user.is_authenticated and current_user.username == 'root':
        try:
            sql_getall = text('SELECT * FROM user;')
            users = db.session.execute(sql_getall)
            return render_template('users.html', pageName="Users List", users=users)
        except sqlalchemy.exc.ProgrammingError:
            return "There are any users"
    else:
        return render_template("access_denied.html")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
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
    session['viewed_articles'] = []
    return redirect(url_for('index'))
