from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
####

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = "secret_key_will_be_here"

login_manager = LoginManager(app)

ckeditor = CKEditor(app)

db = SQLAlchemy(app)

####
migrate = Migrate(app, db)

from app import routes, models
####
