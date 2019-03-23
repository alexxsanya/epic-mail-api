from flask import Flask
from .user import user_api
from .message import msg_api
app = Flask(__name__)
app.register_blueprint(user_api, url_prefix="/api/v1")
app.register_blueprint(msg_api,url_prefix="/api/v1")