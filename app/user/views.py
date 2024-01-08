from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<username>')
def user(username):
    pass # USER PAGE