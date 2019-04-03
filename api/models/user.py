import datetime
from flask import abort, make_response, jsonify, g
from api.util import UserValidator
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token,
    get_jwt_claims, decode_token)

from api.util import DB_Manager
from os import environ


class User():

    db = DB_Manager(
        environ.get("APP_SETTING")
    )

    def __init__(self, email, firstname, lastname, password, recovery_email):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.recovery_email = recovery_email

    def create_user(self):
        if not User.user_exist(self.email):
            query = """
                    INSERT INTO users (
                            firstname,
                            lastname,email,
                            password,
                            recoveryemail
                            )
                            VALUES (
                            '{}', '{}', '{}', '{}', '{}'
                            );
                    """.format(self.firstname, self.lastname,
                               self.email, self.password,
                               self.recovery_email)

            self.db.run_query(query)

            user = User.query_user(self.email)

            if user != []:
                token = create_access_token(identity=user[0].get('id'))
                return abort(
                    jsonify({
                        'status': 201,
                        'data': [{
                            'token': token,
                            'user': {
                                'id': user[0].get('id'),
                                'firstname':user[0].get('firstname')
                            }
                        }]
                    })
                )

        abort(jsonify({
            'status': 400,
            'error': 'Your Email address already exist in the system'
        }))

    @staticmethod
    def user_exist(email):
        query = f"""
                    SELECT email FROM users WHERE
                        email = '{email}';
                """
        result = User.db.run_query(query, query_option='fetch_all')

        if result != []:
            return True

    @staticmethod
    def check_user_id(id):
        query = f"""
                    SELECT id FROM users WHERE
                        id = {id};
                """
        result = User.db.run_query(query, query_option='fetch_all')

        if result != []:
            return True
        abort(jsonify({
            "error": 400,
            "message": "User with id-{} doesn'\t exist".format(id)
        }))

    @staticmethod
    def query_user(email):
        query = f"""
                    SELECT * FROM users WHERE
                        email = '{email}';
                """
        return User.db.run_query(query, query_option='fetch_all')

    @staticmethod
    def login_user(email, password):

        if (UserValidator.is_email_valid(email) and
                UserValidator.is_pass_valid(password)):
            query = f"""
                        SELECT * FROM users WHERE
                            email = '{email}';
                    """
            user = User.db.run_query(query, query_option='fetch_all')

            if len(user) == 1:
                token = create_access_token(identity=user[0]['id'])
                abort(
                    jsonify({
                        'status': 200,
                        'data': [{
                            'token': token,
                            'user': {
                                'id': user[0]['id'],
                                'firstname':user[0]['firstname']
                            }
                        }]
                    })
                )
        return False

    @staticmethod
    def get_user_id(email):
        if UserValidator.is_email_valid(email):

            query = f"""
                        SELECT id FROM users WHERE
                            email = '{email}';
                    """
            user = User.db.run_query(query, query_option='fetch_all')

            if len(user) == 1:
                return user[0]['id']

            abort(jsonify({
                'status': '400',
                'error': 'user {} doesn\'t exist'.format(email)
            }))

    @staticmethod
    def get_user_email(id):
        query = f"""
                    SELECT email FROM users WHERE
                        id = {id};
                """
        result = User.db.run_query(query, query_option='fetch_all')

        if result != []:
            return result[0]['email']
        abort(jsonify({
            "error": 400,
            "message": "User with id-{} doesn'\t exist".format(id)
        }))

    @staticmethod
    def get_all_users():
        query = """
                    SELECT id, email,firstname,lastname
                    FROM users;
                """
        users = User.db.run_query(query, query_option='fetch_all')
        abort(jsonify({
            "status": 200,
            "data": users
        }))
