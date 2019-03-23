from flask import Blueprint,jsonify, request, Response
from api.models import Message
from api.util import MessageValidator
msg_api = Blueprint("msg_api", __name__)

@msg_api.route('/messages',methods=['POST'])
def send_message():
    msg = request.get_json()
    if not msg: 
        return jsonify({
            'error':'Invalid Request Body',
            'status': 400
        })

    if MessageValidator().validator(msg):
        Message(
            subject = msg.get('subject',None),
            msgBody= msg.get('msgBody',None),
			parentId = msg.get('parentId',None),
            sender = msg.get('sender',None),
            reciever = msg.get('reciever',None)
        ).send_message()
