from flask import Blueprint

articles_bp = Blueprint('articles', __name__)

@articles_bp.route('/new/article')
def new_article():
    pass # NEW ARTICLE