import pytest
import json,jwt
from api import app
from api.util import Auth
class TestAuth():
    valid_token = None
    def test_encode_token_works(self):
        TestAuth.valid_token = Auth().encode_token('alex')
        assert len(TestAuth.valid_token) > 20

    @pytest.mark.xfail(raises=jwt.exceptions.DecodeError)
    def test_decode_token_with_incorrect(self):
        Auth().decode_token(83292)

    def test_decode_token_return_correct(self):
        user = Auth().decode_token(TestAuth.valid_token.decode('utf-8'))
        assert user == 'alex'

class TestUserSignupAPI:  
    
    def test_index(self,client):
        response = client.get('/')
        assert response.status_code == 404

    def test_create_user_pass_with_correct_fields(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@epicc.com",
                    "firstname": "alex",
                    "lastname": "Ssanya",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert response.status_code == 200

    def test_create_user_pass_with_incorrect_email(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexxepicc.com",
                    "firstname": "alex",
                    "lastname": "Ssanya",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Incorrect email format" in response.data

    def test_create_user_dont_pass_with_same_email(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@epicc.com",
                    "firstname": "alex",
                    "lastname": "Ssanya",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Your Email address already exist in the system" in response.data

    def test_create_user_dont_pass_with_incorect_password(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@epicc.com",
                    "firstname": "alex",
                    "lastname": "Ssanya",
                    "password": "Alex1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Password should be atleast 6 char" in response.data
    
    def test_create_user_dont_pass_with_incorect_firstname(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@ecc.com",
                    "firstname": "a",
                    "lastname": "Ssanya",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Firstname should be atleast 2 letters without numbers" in response.data
    
    def test_create_user_dont_pass_with_incorect_lastname(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@ppecc.com",
                    "firstname": "alex",
                    "lastname": "",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Lastname should be atleast 2 letters without numbers" in response.data

    def test_create_user_dont_pass_with_same_last_firstname(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@pecc.com",
                    "firstname": "Sanya",
                    "lastname": "sanya",
                    "password": "Alex@1",
                    "recovery_email": "alex@pic.com"
                },
            content_type='application/json')
        assert b"Firstname & Lastname can not be the same" in response.data
    
    def test_create_user_dont_pass_with_same_recoverymail_email(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alexx@peccc.com",
                    "firstname": "Denis",
                    "lastname": "Aalex",
                    "password": "Alex@1",
                    "recovery_email": "alexx@peccc.com"
                },
            content_type='application/json')
        assert b"Recovery email & your choosen email" in response.data

    def test_create_user_dont_pass_with_incorrect_recovery_mail(self,client):
        response = client.post(
            '/api/v1/auth/signup',
            json={
                    "email": "alex@peccc.com",
                    "firstname": "Denis",
                    "lastname": "Aalex",
                    "password": "Alex@1",
                    "recovery_email": "alexxpeccc.com"
                },
            content_type='application/json')
        assert b"Recovery Email has an incorrect email format" in response.data
