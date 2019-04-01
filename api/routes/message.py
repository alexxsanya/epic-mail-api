from flask import Blueprint, jsonify, request, Response
from api.models import Message
from api.util import MessageValidator
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
msg_api = Blueprint("msg_api", __name__)


@msg_api.route('/messages', methods=['POST'])
@jwt_required
def send_message():
    msg = request.get_json()
    if not msg:
        return jsonify({
            'error': 'Invalid Request Body',
            'status': 400
        })

    if MessageValidator().validator(msg):
        return Message(
            subject=msg.get('subject', None),
            msgBody=msg.get('msgBody', None),
            parentId=msg.get('parentId', 0),
            receiver=msg.get('receiver', None)
        ).send_message()


@msg_api.route('/messages', methods=['GET'])
@jwt_required
def get_all_recieved():
    received = Message.get_received_messages()
    return jsonify({
        'data': received,
        'status': 200,
        'info': 'Messages successfully retrieved'
    })


@msg_api.route('/messages/<int:message_id>')
@jwt_required
def get_specific_message(message_id):

    msg = Message.get_one_message(message_id)

    return jsonify({
        'data': msg,
        'status': 200,
        'info': 'Message successfully retrieved'
    })


@msg_api.route('/messages/unread', methods=['GET'])
@jwt_required
def get_all_unread():
    unread = Message.get_unread_messages()
    return jsonify({
        'status': 200,
        'data': unread,
        'info': 'Unread messages successfully retrieved'
    })


@msg_api.route('/messages/sent', methods=['GET'])
@jwt_required
def get_all_sent():
    sent = Message.get_sent_messages()

    return jsonify({
        'status': 200,
        'data': sent,
        'info': 'Sent messages successfully retrieved'
    })


@msg_api.route('/messages/<int:message_id>', methods=['DELETE'])
@jwt_required
def delete_message(message_id):
    Message().delete_message(message_id)
