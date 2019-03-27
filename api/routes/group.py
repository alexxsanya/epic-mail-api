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
    if not group: 
        return jsonify({
            'error':'Invalid Request Body',
            'status': 400
        })

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