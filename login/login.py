from hashlib import md5

from flask import Blueprint, request, make_response, session

from repository.user_repository import UserRepository

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def user_login():
    username = request.forms('username')
    password = request.forms('password')
    user_repository = UserRepository()
    user = user_repository.check_user_login(username, password)
    if user is None:
        return make_response("Not Authorized"), 401
    else:
        session['session_token'] = md5(username + password).digest()
        return make_response("Logged in"), 200
