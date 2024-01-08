from flask import Flask
from config import config
from .main.views import main_bp
from .user.views import user_bp
from .articles.views import articles_bp
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(articles_bp)

    return app