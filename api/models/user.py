import datetime
from flask import abort, make_response, jsonify
from api.util import Auth,UserValidator
class User():

    user_db = []

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
            token = Auth().encode_token(self.email)
            
            return abort(
                jsonify({
                'status':200,
                'data':[{
                        'token':token.decode("utf-8"),
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
    def get_user(user_email):
        if UserValidator.validate_email(user_email):
            user = [u for u in User.user_db if u['email'] == user_email]
            if len(user) == 1:
                return user       

    @staticmethod
    def user_exist(email):
        if email in str(User.user_db):
            return True
        return False
