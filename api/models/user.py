import datetime
from flask import abort, make_response, jsonify,g
from api.util import UserValidator
from flask_jwt_extended import (
    JWTManager, jwt_required, 
    create_access_token, 
    get_jwt_claims, decode_token)
    
class User():

    user_db = [{
        'id':1,
        'email':'alex@epicmail.com',
        'lastname':'alex',
        'firstname':'James',
        'recovery_email':'james@gmail.com',
        'password':'Alex@11'
        },{
        'id':2,
        'email':'steven@epicmail.com',
        'lastname':'steven',
        'firstname':'walton',
        'recovery_email':'walton@gmail.com',
        'password':'Walton@2'            
        }]

    def __init__(self,email,firstname,lastname,password,recovery_email):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.recovery_email = recovery_email

    def create_user(self):
        if not self.user_exist(self.email):
            self.id = len(self.user_db)+1
            self.user_db.append({
                'id':self.id,
                'email':self.email,
                'firstname':self.firstname,
                'lastname':self.lastname,
                'password':self.password,
                'recovery_email':self.recovery_email
            })            
            token = create_access_token(identity=self.id)
            return abort(
                jsonify({
                'status':201,
                'data':[{
                        'token':token,
                        'user':{
                            'id':self.id,
                            'firstname':self.firstname
                        } 
                    }]
                })
            )
        
        abort(jsonify({
            'status':400,
            'error':'Your Email address already exist in the system'
        }))

    @staticmethod
    def user_exist(email):
        if email in str(User.user_db):
            return True
        return False

    @staticmethod
    def login_user(email,password):
         
        if ( UserValidator.is_email_valid(email) and \
                UserValidator.is_pass_valid(password)):

            user = [u for u in User.user_db if ((u['email'] == email) \
                    and (u['password'] == password))]
            if len(user) == 1:
                token = create_access_token(identity=user[0]['id'])
                abort(
                    jsonify({
                    'status':200,
                    'data':[{
                            'token':token,
                            'user':{
                                'id':user[0]['id'],
                                'firstname':user[0]['firstname']
                            }
                        }]
                    })
                )
        return False

    @staticmethod
    def get_user_id(email):
        if UserValidator.is_email_valid(email):
            user = [user for user in User.user_db if user['email'] == email]
            if len(user) == 1:
                return user[0]['id']
            abort(jsonify({
                'status':'400',
                'error':'user {} doesn\'t exist'.format(email)
            }))