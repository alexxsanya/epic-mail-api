import pytest
import json,jwt
from api.models import User
class TestAuth():
    valid_token = None
    def test_api_to_doc(self,client):
        response = client.get('api/v1/doc')
        assert response.status_code == 302    

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
        assert b"Invalid email format for" in response.data

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
        assert b"Invalid email format for" in response.data

    def test_get_user_id(self,client):
        user_id = User.get_user_id('alex@epicmail.com')
        assert user_id == 1

class TestUserSigninAPI:
    User.user_db.append({
        'id':2183,
        'email':'tests@epicmail.com',
        'firstname':'Test User',
        'lastname':'Test',
        'password':'Test@123',
        'recovery_email':'tests1@epicmail.com'
    })
    def test_login_pass_correct_cred(self,client):
        response = client.post(
            '/api/v1/auth/login',
            json={
                    "email": "tests@epicmail.com",
                    "password": "Test@123",
                },
            content_type='application/json')
        assert response.status_code == 200        
    
    def test_login_pass_incorrect_pass_format(self,client):
        response = client.post(
            '/api/v1/auth/login',
            json={
                    "email": "test@epicmail.com",
                    "password": "Test123",
                },
            content_type='application/json')
        assert b'Password should be atleast 6 char' in response.data

    def test_login_pass_incorrect_cred(self,client):
        response = client.post(
            '/api/v1/auth/login',
            json={
                    "email": "teste@picmailcom",
                    "password": "Test@123",
                },
            content_type='application/json')
        assert b'Invalid email format for' in response.data
    def test_login_pass_inexistent_user(self,client):
        response = client.post(
            '/api/v1/auth/login',
            json={
                    "email": "tested@picmail.com",
                    "password": "Test@123",
                },
            content_type='application/json')
        assert b'No user with supplied password or ' in response.data