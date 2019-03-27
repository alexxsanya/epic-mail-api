import datetime
from flask import abort, make_response, jsonify
from .user import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from api.util import DB_Manager
from os import environ 

class Group:

    db = DB_Manager(
            environ.get("APP_SETTING",'development')
        ) 

    def __init__( self,name='',role=''):
        self.name = name
        self.role = role
        self.user_id = get_jwt_identity()

    def create_group(self):
        query = """
                INSERT INTO groups (
                    name,role,createdby 
                )
                VALUES ('{}', '{}', {}) RETURNING *;
                """.format( self.name,
                            self.role,
                            self.user_id,)
        if not self.is_group_exist():
            q = self.db.run_query(query,'fetch_all')
            groups = [g for g in q if g['createdby']==self.user_id]
            return jsonify({
                            'status':201,
                            'data' : groups
                        })
        abort(jsonify({
            'status':400,
            'error' : "Group name - {} exists".format(self.name)
        }))
    
    def is_group_exist(self):
        query = """
                    SELECT id FROM groups
                        WHERE name = '{}'
                """.format(self.name)
        result = self.db.run_query(query,'fetch_all')
        
        if result == []:
            return False
        return True

    def get_groups(self):
        query = """
                SELECT * FROM groups
                    WHERE createdby={}
                """.format(self.user_id)
        groups = self.db.run_query(query,'fetch_all')

        return jsonify({
            'status':200,
            'data': groups
        })
