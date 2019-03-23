import pytest
from flask import url_for
import json,jwt
from api import app
from api.util import Auth
from api.models import User

class TestMessageAPI:
    
    message = {
                "subject":"Hey Brain",
                "reciever":"alex@epicmail.com",
                "sender":"steven@epicmail.com",
                "msgBody":"I juest wanted to say hello to you"
            } 

    def test_message_sent_with_correct_fields(self,client):

        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')
        assert response.status_code == 200        

    def test_message_sent_with_incorrect_subject(self,client):
        self.message['subject'] = " "
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')
        assert b'can not be this small in length' in response.data 

    def test_message_sent_with_incorrect_body(self,client):
        self.message['subject'] = "Hey Brain"
        self.message['msgBody'] = "He"
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')
        assert b'can not be this small in length' in response.data 

    def test_message_sent_with_incorrect_status(self,client):
        self.message['msgBody'] = "I am comming over there"
        self.message['status'] = 'dead'
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')
        assert b'not an acceptable status' in response.data 
    
    def test_message_sent_with_correct_sender_receiver_bt_in_sys(self,client):
        self.message['reciever'] = 'alex@gmail.com'
        self.message['sender'] = 'david@gmail.com'
        self.message['status'] = 'draft'
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')
        assert b'user david@gmail.com doesn\'t exist' in response.data 

    def test_api_with_no_requester_body(self,client):
        response = client.post(
            url_for('msg_api.send_message'),
            json={},
            content_type='application/json')
        assert b'Invalid Request Body' in response.data     
