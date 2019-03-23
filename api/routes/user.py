from flask import Blueprint,jsonify, request, Response
from api.models import User
from api.util import UserValidator
user_api = Blueprint("user_api", __name__)

@user_api.route('/auth/signup',methods=['POST'])
def create_user():
    user = request.get_json()
    if UserValidator.validator(user):
        User(
            email = user.get('email'),
            firstname = user.get('firstname'),
            lastname = user.get('lastname'),
            password = user.get('password'),
            recovery_email = user.get('recovery_email')
        ).create_user()