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

class TestRecievedAPI:

    def test_message_recieved_api(self,client):

        response = client.get(
            url_for('msg_api.get_all_recieved'))
        assert response.status_code == 200   

class TestGetSingleMessageAPI:
    message = {
                "subject":"Hey Alex",
                "reciever":"alex@epicmail.com",
                "sender":"steven@epicmail.com",
                "msgBody":"Testing if you can get this message"
            } 

    def send_message(self,client):
        client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json')  

    def test_get_message_by_id(self,client):

        response = client.get('api/v1/messages/1') 
        assert response.status_code == 200   
    
    @pytest.mark.xfail(raises=IndexError)
    def test_get_message_by_inexistent_id(self,client):

        response = client.get('api/v1/messages/100') 
        assert b'No message with supplied message-id' in response.data