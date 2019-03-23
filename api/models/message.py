import datetime
from flask import abort, make_response, jsonify
from .user import User
class Message:

    messages = []
    receivedMessages = []
    sentMessages = []

    def __init__(   self,
                    subject,
                    msgBody,
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

    @staticmethod
    def get_received_messages(reciever_id):
        r_msgs = [msg for msg in Message.receivedMessages \
                    if reciever_id in msg['reciever_id']]

        r_msg_db = []

        for msg in r_msgs:
            mgx = [m for m in Message.messages if msg['message_id'] == m['id']]
            if(len(mgx)>0):
                r_msg_db.append(mgx[0])

        return r_msg_db

    @staticmethod
    def get_unread_messages(reciever_id):
        r_msgs = Message.get_received_messages(reciever_id)
        unread_msg = [msg for msg in r_msgs if msg['status']=='unread']
        return unread_msg

    @staticmethod
    def get_sent_messages(sender_id):
        s_msgs = [msg for msg in Message.sentMessages \
                    if sender_id in msg['sender_id']]

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


    