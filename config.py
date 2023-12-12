# from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/projectflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images/'
    CKEDITOR_SERVE_LOCAL = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # SESSION_TYPE = 'filesystem'
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    # SESSION_KEY_PREFIX = 'projectflask'