from flask import Flask
from .user import user_api
from .message import msg_api
from .group import g_api
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token,
    get_jwt_claims, decode_token)

from config import app_config

from api.util import DB_Manager


def create_app(app_env):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[str(app_env)])
    JWTManager(app)
    DB_Manager(app_env).create_tables()
    app.register_blueprint(user_api, url_prefix="/api/v1")
    app.register_blueprint(msg_api, url_prefix="/api/v1")
    app.register_blueprint(g_api, url_prefix="/api/v1")
    return app
