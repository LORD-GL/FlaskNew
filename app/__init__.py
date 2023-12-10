from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
####
from flask_migrate import Migrate
####

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = "secret_key_will_be_here"

db = SQLAlchemy(app)

####
migrate = Migrate(app, db)

from app import routes, models
####
