from flask import Blueprint, jsonify, request, Response, redirect
from api.models import User
from api.util import UserValidator
user_api = Blueprint("user_api", __name__)


@user_api.route('/auth/signup', methods=['POST'])
def create_user():
    user = request.get_json()
    if UserValidator.validator(user):
        User(
            email=user.get('email'),
            firstname=user.get('firstname'),
            lastname=user.get('lastname'),
            password=user.get('password'),
            recovery_email=user.get('recovery_email')
        ).create_user()


@user_api.route('/auth/login', methods=['POST'])
def login():
    user = request.get_json()
    is_logged = User.login_user(
        email=user.get('email'),
        password=user.get('password')
    )

    if not is_logged:
        return jsonify({
            'error': 'No user with supplied password or email address',
            'status': 400,
        })


@user_api.route('/doc')
def get_api_doc():

    return redirect("https://epicmailapi.docs.apiary.io")
