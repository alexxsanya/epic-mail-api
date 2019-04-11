import datetime
from flask import abort, make_response, jsonify
from .user import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from api.util import DB_Manager
from os import environ


class Message:

    db = DB_Manager(
        environ.get("APP_SETTING")
    )

    def __init__(self,
                 subject='',
                 msgBody='',
                 status="draft",
                 createdOn=None,
                 receiver=0,
                 id=0,
                 parentId=0,
                 is_group_mail=False,
                 group_id=0
                 ):
        self.id = id,
        self.createdOn = createdOn
        self.subject = subject
        self.msgBody = msgBody
        self.parentId = parentId
        self.status = status
        self.receiver = receiver
        self.sender_id = get_jwt_identity()
        self.is_group_mail = is_group_mail
        self.group_id = group_id

    def create_message(self):
        createdby = self.sender_id
        if self.parentId is None:
            self.parentId = 0
        if self.is_group_mail:
            createdby = self.group_id
        query = """
                INSERT INTO messages (
                    subject,msgbody,
                    parentid,status,
                    createdby,isgroupmail
                )
                VALUES (
                    '{}', '{}', {}, '{}', {},{}
                    ) RETURNING *;
                """.format(self.subject,
                           self.msgBody, int(self.parentId),
                           self.status,
                           createdby,
                           self.is_group_mail)
        status = self.db.run_query(query)
        return jsonify({
            'status': 201,
            'data': str(status),
            'message': 'message saved as draft'
            })

    def send_message(self):
        self.create_message()

        message_id = self.get_message_id()

        Message.update_message_status(message_id, 'sent')

        self.log_in_messages_received(message_id)

        self.log_in_messages_sent(message_id)

        return jsonify({
            'status': 201,
            'data': {
                'message_id': message_id,
                'message': 'Message successfully sent to {}'
                .format(self.receiver)
            }
        })

    def log_in_messages_sent(self, message_id):
        sent_q = """
                INSERT INTO messages_sent (
                    senderid,messageid
                )
                VALUES (
                    '{}', '{}'
                    );
                """.format(self.sender_id,
                           message_id)
        self.db.run_query(sent_q)

    def log_in_messages_received(self, message_id):
        receiver = self.receiver
        if not isinstance(receiver, int):
            receiver = User.get_user_id(self.receiver)
        rec_q = """
                INSERT INTO messages_received (
                    receiverid,messageid
                )
                VALUES (
                    '{}', '{}'
                    );
                """.format(receiver, message_id)

        self.db.run_query(rec_q)

    def get_message_id(self):
        query = """
                SELECT id FROM messages WHERE
                    subject='{}' AND createdby='{}';
                """.format(self.subject,
                           self.sender_id
                           )

        message = self.db.run_query(query, 'fetch_all')

        if message != []:
            return message[0]['id']
        abort(jsonify({
            'status': 400,
            'error': 'No Message with subject {}'.format(self.subject)
        }))

    @staticmethod
    def get_received_messages():
        receiver_id = get_jwt_identity()

        received_log = Message.query_a_table('messages_received',
                                             'receiverid',
                                             receiver_id)

        recieved_db = []

        for msg in received_log:

            mgx = Message.query_a_table('messages', 'id', msg['messageid'])

            if(len(mgx) > 0):

                sender_log = Message.query_a_table('messages_sent',
                                                   'messageid', mgx[0]['id'])

                mgx[0]['createdby'] = sender_log[0]['senderid']

                recieved_db.append(mgx[0])

        return recieved_db

    @staticmethod
    def get_unread_messages():
        r_msgs = Message.get_received_messages()

        unread_msg = [msg for msg in r_msgs
                      if(msg['status'] == 'sent' and msg['readstatus'] == 'unread')]

        return unread_msg

    @staticmethod
    def get_draft_messages():
        user_id = get_jwt_identity()
        msg_query = """
                SELECT * FROM messages WHERE
                    createdby={} AND status='draft';
                """.format(user_id)
        result = Message.db.run_query(msg_query, 'fetch_all')
        return result

    @staticmethod
    def get_sent_messages():
        sender_id = get_jwt_identity()

        sent_log = Message.query_a_table('messages_sent',
                                         'senderid',
                                         sender_id)
        msg_db = Message.query_a_table('messages',
                                       'createdby',
                                       sender_id)
        sent_msg_db = []

        for msg in sent_log:
            mgx = [m for m in msg_db if m['id'] == msg['messageid']]
            rec_log = Message.query_a_table('messages_received',
                                            'messageid',
                                            msg['messageid'])
            if(len(rec_log) > 0):
                mgx[0]['receiverid'] = rec_log[0]['receiverid']
            sent_msg_db.append(mgx[0])

        return sent_msg_db

    @staticmethod
    def update_message_status(msg_id, status):
        update_m = """
                    UPDATE messages SET status='{}'
                        WHERE id = {}
                   """.format(status, msg_id)
        Message.db.run_query(update_m)

    @staticmethod
    def update_message_read_status(msg_id):
        update_m = """
                    UPDATE messages SET readstatus='read'
                        WHERE id = {}
                   """.format(msg_id)
        Message.db.run_query(update_m)

    @staticmethod
    def get_one_message(msg_id):
        c_user = get_jwt_identity()
        try:
            _msg = Message.query_a_table('messages',
                                         'id',
                                         msg_id)
            _sender = Message.query_a_table('messages_sent',
                                            'messageid',
                                            msg_id)
            _receiver = Message.query_a_table('messages_received',
                                              'messageid',
                                              msg_id)
            _msg[0]['senderid'] = _sender[0]['senderid']

            Message.update_message_read_status(msg_id)

            if(len(_receiver) > 0):
                _msg[0]['receiverid'] = _receiver[0]['receiverid']
                _msg[0]['sender'] = User.get_user_email(_sender[0]['senderid'])
                if _msg[0]['receiverid'] == c_user or \
                        _msg[0]['senderid'] == c_user:
                    return _msg
            return _msg

        except IndexError:
            abort(jsonify({
                'status': 204,
                'error': 'No message with supplied message-id {}'.format(
                    msg_id
                )
            }))

    def delete_message(self, msg_id):
        user_id = get_jwt_identity()

        _msg = Message.query_a_table('messages',
                                     'id',
                                     msg_id)
        _sender = Message.query_a_table('messages_sent',
                                        'messageid',
                                        msg_id)
        _receiver = Message.query_a_table('messages_received',
                                          'messageid',
                                          msg_id)
        if len(_msg) > 0 and len(_sender):

            if user_id == _sender[0]['senderid'] or\
                    user_id == _receiver[0]['receiverid']:

                if user_id == _sender[0]['senderid']:
                    a = Message.delete_from_table('messages_sent', 'messageid',
                                                  msg_id)
                    print("deleted -> {}".format(a))
                if len(_receiver) > 0:
                    Message.delete_from_table('messages_received', 'messageid',
                                              msg_id)

                abort(jsonify({
                    'status': 200,
                    'data': {
                        'message': 'Message {} has been deleted'.format(msg_id)
                    }
                }))
            abort(jsonify({
                'status': 401,
                'message': 'You are not permitted to delete this message'
            }))
        abort(jsonify({
            'status': 204,
            'error': 'No message with provided id - {} '.format(msg_id)
        }))

    @staticmethod
    def query_a_table(table, column, value):
        msg_query = """
                SELECT * FROM {} WHERE
                    {}={};
                """.format(table, column, value)
        return Message.db.run_query(msg_query, 'fetch_all')

    @staticmethod
    def delete_from_table(table, column, value):
        msg_query = """
                DELETE FROM {} WHERE
                    {}={};
                """.format(table, column, value)
        return Message.db.run_query(msg_query)
