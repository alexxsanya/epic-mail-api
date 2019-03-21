import datetime 
from functools import wraps
import jwt

class Auth():

    def __init__(self):
        pass
    @staticmethod
    def encode_token(user_name):  
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + \
                        datetime.timedelta(seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_name
            }
            return jwt.encode(
                payload,
                "secretme",
                algorithm='HS256'
            )
        except Exception as error:
            return error

    def decode_token(self,token):
        try:
            payload = jwt.decode(token, 'secretme', algorithms=['HS256'])
            return payload['sub']
        except (Exception, jwt.exceptions.DecodeError) as error:
            raise error