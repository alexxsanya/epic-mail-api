import pytest
from flask import url_for
import json,jwt
from api import app
from api.models import Message

@pytest.fixture     
def user_token(client): 
    response = client.post('/api/v1/auth/login', 
                    content_type='application/json', 
                    json={
                        "email" : "alex@epicmail.com",
                        "password": "Alex@11",
                    })
    access_token = json.loads(response.data.decode())
    access_token = access_token['data'][0]['token']
    return access_token

class TestMessageAPI:
    
    message = {
                "subject":"Hey Brain",
                "reciever":"alex@epicmail.com",
                "sender":"steven@epicmail.com",
                "msgBody":"I juest wanted to say hello to you"
            } 

    def test_message_sent_with_correct_fields(self,client,user_token):
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert response.status_code == 200        
    
    def test_message_sent_with_incorrect_subject(self,client,user_token):
        self.message['subject'] = " "
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert b'can not be this small in length' in response.data 

    def test_message_sent_with_incorrect_body(self,client,user_token):
        self.message['subject'] = "Hey Brain"
        self.message['msgBody'] = "He"
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert b'can not be this small in length' in response.data 

    def test_message_sent_with_incorrect_status(self,client,user_token):
        self.message['msgBody'] = "I am comming over there"
        self.message['status'] = 'dead'
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert b'not an acceptable status' in response.data 
    
    def test_message_sent_with_correct_sender_receiver_bt_in_sys(self,client,user_token):
        self.message['reciever'] = 'alex@gmail.com'
        self.message['sender'] = 'david@gmail.com'
        self.message['status'] = 'draft'
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert b'user david@gmail.com doesn\'t exist' in response.data 

    def test_api_with_no_requester_body(self,client,user_token):
        token = user_token
        response = client.post(
            url_for('msg_api.send_message'),
            json={},
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
        assert b'Invalid Request Body' in response.data     

class TestRecievedAPI:

    def test_message_recieved_api(self,client,user_token):
        token = user_token
        response = client.get(
            url_for('msg_api.get_all_recieved'),
            headers=dict(Authorization='Bearer ' + token))
        assert response.status_code == 200   

class TestGetSingleMessageAPI:
    message = {
                "subject":"Hey Alex",
                "reciever":"alex@epicmail.com",
                "sender":"steven@epicmail.com",
                "msgBody":"Testing if you can get this message"
            } 

    def send_message(self,client,user_token):
        token = user_token
        client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))  

    def test_get_message_by_id(self,client,user_token):
        token = user_token
        response = client.get('api/v1/messages/1',
            headers=dict(Authorization='Bearer ' + token)) 
        assert response.status_code == 200   
    
    @pytest.mark.xfail(raises=IndexError)
    def test_get_message_by_inexistent_id(self,client,user_token):
        token = user_token
        response = client.get('api/v1/messages/100',
            headers=dict(Authorization='Bearer ' + token)) 
        assert b'No message with supplied message-id' in response.data

class TestGetAllUnreadAPI:
    def test_get_all_unread(self,client,user_token):
        token = user_token
        response = client.get('api/v1/messages/unread',
            headers=dict(Authorization='Bearer ' + token)) 
        assert response.status_code == 200         

class TestGetAllSentAPI:
    def test_get_all_sent(self,client,user_token):
        token = user_token
        response = client.get('api/v1/messages/sent',
            headers=dict(Authorization='Bearer ' + token)) 
        assert response.status_code == 200         

class TestDeleteMessageAPI: 
    message = {
                "subject":"Hey Brain",
                "reciever":"alex@epicmail.com",
                "sender":"alex@epicmail.com",
                "msgBody":"I juest wanted to say hello to you"
    } 

    def test_message_sent_with_correct_fields(self,client,user_token):
        token = user_token
        client.post(
            url_for('msg_api.send_message'),
            json=self.message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

    def test_delete_message_with_non_message(self,client,user_token):
        token = user_token
        response = client.delete(
            '/api/v1/messages/2',
            headers=dict(Authorization='Bearer ' + token)) 
        assert b'No message with provided id ' in response.data  

    def test_delete_my_message(self,client,user_token):
        token = user_token
        response = client.delete(
            '/api/v1/messages/1',
            headers=dict(Authorization='Bearer ' + token)) 
        assert b'has been deleted' in response.data  