from flask import Blueprint,jsonify, request, Response
from api.models import Group
from api.util import GroupValidator
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
g_api = Blueprint("g_api", __name__)

@g_api.route('/groups',methods=['POST'])
@jwt_required
def create_group():
    group = request.get_json()

    if GroupValidator().validator(**group):
        return Group(
              name=group.get('name'),
              role=group.get('role')
            ).create_group()
    
@g_api.route('/groups',methods=['GET'])
@jwt_required
def get_groups():
    return Group().get_groups()

@g_api.route('/groups/<int:group_id>/<string:name>',methods=['PATCH'])
@jwt_required
def upfate_group_name(group_id,name):
    return Group(
            group_id=group_id,
            name=name
        ).update_group_name()

@g_api.route('/groups/<int:group_id>',methods=['DELETE'])
@jwt_required
def delete_group(group_id):
    return Group(
            group_id=group_id
        ).delete_group()

@g_api.route('/groups/<int:group_id>/users',methods=['POST'])
@jwt_required
def add_user_to_group(group_id):
    user = request.get_json()
    return Group.add_user_to_group(
        user_id = user.get('user_id'),
        user_role = user.get('user_role'),
        group_id = group_id
    )

@g_api.route('/groups/<int:group_id>/users/<int:user_id>',methods=['DELETE'])
@jwt_required
def remove_user_from_group(group_id,user_id):
    return Group.remove_user(
        user_id = user_id,
        group_id = group_id
    )

@g_api.route('/groups/<int:group_id>/messages',methods=['POST'])
@jwt_required
def send_group_mail(group_id):
    message = request.get_json()
    return Group.send_group_email(
        group_id,
        **message
    )