from flask import Blueprint, flash, session
from flask import render_template, request, url_for, redirect
from app.decorators import login_required
from .funcs import allowed_file
from flask_login import current_user
from app.db_utils.article_utils import add_article
from app.forms.forms import NewsForm
import os 

articles_bp = Blueprint('articles', __name__)


@articles_bp.context_processor
def inject_global_variables():
    from app.models import Theme
    from app.cca import CCA
    themes = Theme.query.all()
    return dict(themes=themes, ARTICLES_PER_PAGE=CCA.ARTICLES_PER_PAGE)


@articles_bp.route('/new/article', methods=['GET', 'POST'])
@login_required
def new_article():
    from app.models import Theme
    from app import db, app
    themes = Theme.query.all()
    if request.method == 'POST':
        image = request.files['file']
        if allowed_file(image.filename):
            new_article = add_article(request.form['title'], request.form['description'], request.form['content'], request.form['author'], current_user)
            if new_article is False:
                return render_template('articles/new_article.html', message="Something went wrong during creating new Article")
            else:
                selected_themes_ids = request.form.getlist('themes')
                for id in selected_themes_ids:
                    selected_theme = Theme.query.filter_by(id=int(id)).first()
                    new_article.themes.append(selected_theme)
                ##########################################
                image_name = str(new_article.id) + "."
                image_name += '.' in image.filename and image.filename.rsplit('.', 1)[1].lower()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
                new_article.image = "images/"+image_name
                db.session.commit()
                # flash('Article successfully uploaded')
                return redirect(url_for('articles.article', id=new_article.id))
        else:
            return render_template('articles/new_article.html', message="Image format isn't supporting", themes=themes)
    else:
        return render_template('articles/new_article.html', message="", themes=themes, pageName="New Article")


@articles_bp.route('/delete/article/<int:id>')
@login_required
def delete_article(id):
    from app.models import Article
    from app import db
    article = Article.query.get_or_404(id)
    if current_user.username == "root" or current_user.id == article.author_account.id:
        db.session.delete(article)
        db.session.commit()
        flash("Article has been succesfully deleted")
        return redirect(url_for('main.index'))
    else:
        return render_template("errors/access_denied.html")


@articles_bp.route('/edit/article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    from app.models import Theme, Article
    from app import db, app
    article = Article.query.get_or_404(id)
    themes = Theme.query.all()
    if current_user.username == "root" or current_user.id == article.author_account.id:
        form = NewsForm(obj=article)
        if form.validate_on_submit():
            form.populate_obj(article)
            article.title = form.title.data
            article.description = form.description.data
            article.content = form.content.data
            article.author = form.author.data
            selected_themes = form.themes.data
            article.themes = []
            for selected_theme in selected_themes:
                article.themes.append(selected_theme)
            try:
                image_name = str(article.id) + "."
                image_name += '.' in form.image.data.filename and form.image.data.filename.rsplit('.', 1)[1].lower()
                form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
                article.image = "images/"+image_name
            except AttributeError:
                pass
            else:
                render_template('articles/edit_article.html', form=form, article=article, themes=themes, message="Error during saving the image", pageName="Edit Article")
            finally:
                db.session.commit()
                return redirect(url_for("articles.article", id = article.id))
        return render_template('articles/edit_article.html', form=form, article=article, themes=themes, pageName="Edit Article")
    else:
        return render_template("errors/access_denied.html", pageName="Error")



@articles_bp.route('/article/<int:id>')#, methods=['POST', 'GET'])
def article(id):
    from app.models import Article
    from app import db
    article = Article.query.get_or_404(int(id))
    viewed_articles_key = 'viewed_articles'
    if viewed_articles_key not in session:
        session[viewed_articles_key] = []
    if id not in session[viewed_articles_key]:
        article.views += 1
        session[viewed_articles_key].append(id)
        db.session.commit()
        session.modified = True

    return render_template("articles/article.html", article = article, pageName="Article")
