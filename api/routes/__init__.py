from flask import Flask, render_template
from .user import user_api
from .message import msg_api
from .group import g_api
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token,
    get_jwt_claims, decode_token)

from config import app_config

from api.util import DB_Manager

from flask_cors import CORS


def create_app(app_env):

    app = Flask(__name__, instance_relative_config=True)

    @app.route('/', methods=['GET'])
    def home():
        return render_template("index.html")

    @app.route('/login.html', methods=['GET'])
    def login():
        return render_template("login.html")

    @app.route('/signup.html', methods=['GET'])
    def signup():
        return render_template("signup.html")

    @app.route('/components/groups.html', methods=['GET'])
    def group():
        return render_template("./components/groups.html")

    @app.route('/components/compose.html', methods=['GET'])
    def compose():
        return render_template("./components/compose.html")

    app.config.from_object(app_config[str(app_env)])
    JWTManager(app)
    DB_Manager(app_env).create_tables()
    app.register_blueprint(user_api, url_prefix="/api/v1")
    app.register_blueprint(msg_api, url_prefix="/api/v1")
    app.register_blueprint(g_api, url_prefix="/api/v1")

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app
