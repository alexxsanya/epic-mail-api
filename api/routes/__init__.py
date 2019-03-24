from flask import Flask
from .user import user_api
from .message import msg_api
from flask_jwt_extended import (
    JWTManager, jwt_required, 
    create_access_token, 
    get_jwt_claims, decode_token)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'my_secrete_key'
jwt = JWTManager(app)
app.register_blueprint(user_api, url_prefix="/api/v1")
app.register_blueprint(msg_api,url_prefix="/api/v1")