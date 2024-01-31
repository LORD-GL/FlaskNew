from flask import Blueprint
from flask import render_template, request, url_for
from .funcs import get_filtered_articles
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import desc

from app.cca import CCA

main_bp = Blueprint('main', __name__)


@main_bp.context_processor
def inject_global_variables():
    from app.models import Theme
    from app.cca import CCA
    themes = Theme.query.all()
    return dict(themes=themes, ARTICLES_PER_PAGE=CCA.ARTICLES_PER_PAGE)


@main_bp.route('/')
def index():
    from app.models import Article
    try: 
        page = request.args.get('page', 1, type=int)
        per_page = CCA.ARTICLES_PER_PAGE
        start = (page - 1) * per_page
        end = start + per_page
        all_news = Article.query.all()
        if 'filter' in request.args.keys():
            filter_type = request.args['filter']
            news = get_filtered_articles(filter_type, all_news)[start:end]
        else:
            filter_type = 'new'
            news = Article.query.order_by(desc(Article.creation_date)).all()[start:end]
        news_amount = len(all_news)
        if news_amount % 2 != 0:
            news_amount += 1
        return render_template('main/index.html', pageName="Home Page", url_for_link=url_for('main.index'),
                               news = news, news_page=page, news_amount=news_amount, filter_type=filter_type)
    except ProgrammingError:
        return "Error"
    


@main_bp.route('/theme/<themelink>')
def theme(themelink):
    from app.models import Theme
    page = request.args.get('page', 1, type=int)
    per_page = CCA.ARTICLES_PER_PAGE
    start = (page - 1) * per_page
    end = start + per_page
    theme = Theme.query.filter_by(link = themelink).first()
    if 'filter' in request.args.keys():
            filter_type = request.args['filter']
            articles = get_filtered_articles(filter_type, theme.articles)[start:end]
    else:
        filter_type = 'new'
        articles = theme.articles[start:end]
    news_amount = len(theme.articles)
    if news_amount % 2 != 0:
        news_amount += 1
    if theme:
        return render_template('main/theme.html', articles=articles, url_for_link=url_for('main.theme', themelink=theme.link),
                               pageName=theme.name, news_page=page, theme=theme, news_amount=news_amount, filter_type=filter_type)
    else:
        return render_template('errors/404.html', pageName="Not Found")

