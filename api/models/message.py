import datetime
from flask import abort, make_response, jsonify
from .user import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
class Message:

    messages = []
    receivedMessages = []
    sentMessages = []

    def __init__(   self,
                    subject='',
                    msgBody='',
                    status="draft",
                    createdOn=None,
                    reciever=0,
                    sender=0,
                    id = 0,
                    parentId=0,
                ):
        self.id = id,
        self.createdOn = createdOn
        self.subject = subject
        self.msgBody = msgBody
        self.parentId = parentId
        self.status = status
        self.reciever_id = reciever
        self.sender_id = sender

    def create_message(self):
        self.id = len(self.messages)+1
        self.createdOn = datetime.datetime.now().timestamp()
        self.messages.append({
			'id': self.id,
			'createdOn': str(self.createdOn),
			'subject':self.subject,
            'msgBody':self.msgBody,
			'parentId':self.parentId,
			'status':self.status
        })

    def send_message(self):
        self.create_message()

        Message.update_message_status(self.id,'sent')

        self.sentMessages.append({
			'sender_id': User.get_user_id(self.sender_id),
			'message_id':self.id,
			'createdOn':self.createdOn
		})
        
        self.receivedMessages.append({
            'reciever_id':User.get_user_id(self.reciever_id),
            'message_id':self.id,
            'createdOn': self.createdOn
        })

        abort(jsonify({
            'status':201,
            'data':{
                'message_id': self.id,
                'message': 'Message successfully sent to {}'.format(self.reciever_id)
            }
        }))

    @staticmethod
    def get_received_messages():
        reciever_id = get_jwt_identity()
        r_msgs = [msg for msg in Message.receivedMessages \
                    if reciever_id == msg['reciever_id']]

        r_msg_db = []

        for msg in r_msgs:
            
            mgx = [m for m in Message.messages if msg['message_id'] == m['id']]
            
            if(len(mgx)>0):
                
                sender = [m for m in Message.sentMessages if m['message_id']==reciever_id]
                
                mgx[0]['sender_id'] = sender[0]['sender_id']
                
                r_msg_db.append(mgx[0])

        return r_msg_db

    @staticmethod
    def get_unread_messages():
        r_msgs = Message.get_received_messages()
        unread_msg = [msg for msg in r_msgs if msg['status']=='sent']
        return unread_msg

    @staticmethod
    def get_sent_messages():
        sender_id = get_jwt_identity()
        s_msgs = [msg for msg in Message.sentMessages \
                    if sender_id == msg['sender_id']]

        sent_msg_db = []

        for msg in s_msgs:
            mgx = [m for m in Message.messages if msg['message_id'] == m['id']]
            if(len(mgx)>0):
                sent_msg_db.append(mgx[0])

        return sent_msg_db      

    @staticmethod
    def update_message_status(msg_id,status):
        msg = [m for m in Message.messages if m['id']==msg_id]
        msg[0]['status'] = status

    @staticmethod
    def get_one_message(msg_id):
        try: 
            _msg = [m for m in Message.messages if m['id'] == msg_id]
            sender = [s for s in Message.sentMessages if s['message_id'] == msg_id]
            receiver = [r for r in Message.receivedMessages if r['message_id'] == msg_id]
            _msg[0]['sender_id'] = sender[0]['sender_id']
            _msg[0]['reciever_id'] = receiver[0]['reciever_id']

            return _msg
            
        except IndexError:
            abort(jsonify({
                'status':204,
                'error': 'No message with supplied message-id {}'.format(msg_id)
            }))

    def delete_message(self,msg_id):
        user_id = get_jwt_identity()

        msg_item_record = [m for m in self.messages\
                                if m['id'] == msg_id]
        snt_item_record = [s for s in self.sentMessages\
                                    if s['message_id'] == msg_id]
        rec_item_record = [r for r in self.receivedMessages\
                                    if r['message_id'] == msg_id]
        if len(msg_item_record) > 0 and len(snt_item_record)\
            and len(rec_item_record):
        
            if user_id == snt_item_record[0]['sender_id'] or\
                user_id == rec_item_record[0]['reciever_id']:
                        
                self.messages.remove(msg_item_record[0])
                self.sentMessages.remove(snt_item_record[0])
                self.receivedMessages.remove(rec_item_record[0])

                abort(jsonify({
                    'status':200,
                    'data':{
                        'message':'Message {} has been deleted'.format(msg_id)
                    }
                }))
            abort(jsonify({
                    'status':401,
                    'message':'You are not permitted to delete this message'
            }))
        abort(jsonify({
            'status':204,
            'error':'No message with provided id - {} '.format(msg_id)
        }))