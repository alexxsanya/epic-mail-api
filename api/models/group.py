import datetime
from flask import abort, make_response, jsonify
from .user import User
from .message import Message
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from api.util import DB_Manager
from os import environ


class Group:

    db = DB_Manager(
        environ.get("APP_SETTING")
    )

    def __init__(self, name='', role='', group_id=0):
        self.name = name
        self.role = role
        self.group_id = group_id
        self.user_id = get_jwt_identity()

    def create_group(self):
        query = """
                INSERT INTO groups (
                    name,role,createdby
                )
                VALUES ('{}', '{}', {}) RETURNING *;
                """.format(self.name,
                           self.role,
                           self.user_id,)
        if not self.is_group_exist():
            q = self.db.run_query(query, 'fetch_all')
            groups = [g for g in q if g['createdby'] == self.user_id]
            return jsonify({
                'status': 201,
                'data': groups
            })
        abort(jsonify({
            'status': 400,
            'error': "Group name - {} exists".format(self.name)
        }))

    def is_group_exist(self):
        query = """
                    SELECT id FROM groups
                        WHERE name = '{}'
                """.format(self.name)
        result = self.db.run_query(query, 'fetch_all')

        if result == []:
            return False
        return True

    def get_groups(self):
        query = """
                SELECT * FROM groups
                    WHERE createdby={}
                """.format(self.user_id)
        groups = self.db.run_query(query, 'fetch_all')

        return jsonify({
            'status': 200,
            'data': groups
        })

    def update_group_name(self):
        query = """
                UPDATE groups
                SET name = '{}'
                WHERE id ={} RETURNING *
                """.format(self.name, self.group_id)
        new_group = self.db.run_query(query, 'fetch_all')

        return jsonify({
            'status': 200,
            'data': new_group
        })

    def delete_group(self):
        query = """
                    DELETE FROM groups
                        WHERE id={} RETURNING *
                """.format(self.group_id)
        self.db.run_query(query, 'fetch_all')
        return jsonify({
            'status': 200,
            'message': "message id {} deleted".format(self.group_id)
        })

    @staticmethod
    def group_exists(id):
        query = f"""
                    SELECT id FROM groups WHERE
                        id = '{id}';
                """
        result = Group.db.run_query(query, query_option='fetch_all')

        if result != []:
            return True
        return False

    @staticmethod
    def is_group_owner(user_id, group_id):
        query = """
                SELECT id FROM groups
                    WHERE createdby = {} AND
                    id = {}
                """.format(user_id, group_id)
        rows = Group.db.run_query(query, 'fetch_all')

        if len(rows) == 1:
            return True
        abort(jsonify({
            "error": 400,
            "message": "Have no rights to add to this group"
        }))

    @staticmethod
    def is_user_a_member(user_id, group_id):
        query = """
                SELECT * FROM group_users
                    WHERE userid={} AND
                    groupid={}
                """.format(user_id, group_id)
        rows = Group.db.run_query(query, 'fetch_all')
        if len(rows) == 1:
            return True
        return False

    @staticmethod
    def add_user_to_group(user_id, group_id, user_role):
        c_user = get_jwt_identity()
        if User.check_user_id(user_id) and \
                Group.group_exists(group_id) and\
                Group.is_group_owner(c_user, group_id) and\
                not Group.is_user_a_member(user_id, group_id):
            query = """
                    INSERT INTO group_users (
                        groupid,
                        userid,
                        userrole
                    ) VALUES ({},{},'{}') RETURNING *
                    """.format(
                group_id, user_id, user_role
            )
            ad = Group.db.run_query(query, 'fetch_all')

            return jsonify({
                'status': 200,
                'data': ad
            })
        abort(jsonify({
            "error": 400,
            "message": "User {} is already a member of group {}".format(
                user_id, group_id)
        }))

    @staticmethod
    def remove_user(user_id, group_id):
        c_user = get_jwt_identity()
        if User.check_user_id(user_id) and \
                Group.group_exists(group_id) and\
                Group.is_group_owner(c_user, group_id):

            query = """
                DELETE FROM group_users
                 WHERE groupid={} AND userid={}
                 RETURNING *
            """.format(group_id, user_id)
            Group.db.run_query(query, 'fetch_all')

            return jsonify({
                'status': 200,
                'message': "user {} deleted from group {}".format(
                    user_id, group_id)
            })

    @staticmethod
    def get_group_members(group_id):
        query = """
                    SELECT userid FROM group_users
                     WHERE groupid={}
                """.format(group_id)
        return Group.db.run_query(query, 'fetch_all')

    @staticmethod
    def send_group_email(group_id, **msg):

        if Group.group_exists(group_id):
            group_members = Group.get_group_members(group_id)

            receiver = []
            Message(
                subject=msg.get('subject', None),
                msgBody=msg.get('msgBody', None),
                parentId=msg.get('parentId', 0),
                status='sent',
                is_group_mail=True,
                group_id=group_id
            ).create_message()

            query = """
                    SELECT id FROM messages
                        WHERE subject='{}'
                        AND isgroupmail={} AND
                        createdby='{}'
                """.format(msg.get('subject'), True, group_id)

            message = Group.db.run_query(query, 'fetch_all')

            msg_id = message[0]['id']

            for member in group_members:

                receiver_id = member['userid']

                Message.update_message_status(msg_id, 'sent')

                Group.log_in_messages_received(receiver_id, msg_id)

                Message().log_in_messages_sent(msg_id)

                receiver.append(member)

            return jsonify({
                'status': 200,
                'data': receiver
            })
        return jsonify({
            'error': 400,
            'message': 'No group with id - {}'.format(group_id)
        })

    @staticmethod
    def log_in_messages_received(receiver_id, message_id):

        rec_q = """
                INSERT INTO messages_received (
                    receiverid,messageid
                )
                VALUES (
                    {}, {}
                    );
                """.format(receiver_id, message_id)

        Group.db.run_query(rec_q)

    @staticmethod
    def group_users(group_id):
        c_user = get_jwt_identity()
        if Group.group_exists(group_id):
            group_members = []
            query = """
                SELECT userid,userrole FROM group_users
                 WHERE groupid={}
            """.format(group_id)

            users_query = """
                SELECT id,firstname,lastname FROM users
            """

            group_users = Group.db.run_query(query, 'fetch_all')

            users = Group.db.run_query(users_query, 'fetch_all')

            for g_user in group_users:
   
                member = [u for u in users if (u['id'] == g_user['userid'])]
                member[0]['role'] = g_user['userrole']
                group_members.append(member[0])

            return jsonify({
                'status': 200,
                'data': group_members
            })
        return jsonify({
            'status': 200,
            'data': []
        })
