from flask import Blueprint,jsonify, request, Response
from api.models import User
from api.util import UserValidator
user_api = Blueprint("user_api", __name__)

@user_api.route('/create-user',methods=['POST'])
def create_user():
    user = request.get_json()
    if UserValidator.validator(user):
        result = User(
            email = user.get('email'),
            firstname = user.get('firstname'),
            lastname = user.get('lastname'),
            password = user.get('password'),
            recovery_email = user.get('recovery_email')
        ).create_user()
        
        return jsonify({
            'status':200,
            'data':result
        })
