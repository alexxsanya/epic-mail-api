import pytest
from api import create_app
import json
from api.util import DB_Manager

@pytest.fixture
def app():
    app = create_app("testing")

    return app

@pytest.fixture
def client(app):
    return app.test_client()

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

@pytest.fixture(scope="module")
def db():
    db = DB_Manager('testing')
    db.create_tables
    yield db
    db.drop_tables()
    db.conn.close()

@pytest.fixture()
def create_message(client,user_token):
    message = {
                "subject":"Hey Brain",
                "reciever":"alex@epicmail.com",
                "msgBody":"I juest wanted to say hello to you"
    } 

    token = user_token
    client.post(
            '/api/v1/messages',
            json=message,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))

@pytest.fixture()
def create_user(client,user_token):
    user = {
                   "email": "admin@epicmail.com",
                    "firstname": "admin",
                    "lastname": "nimd",
                    "password": "Admin@1",
                    "recovery_email": "alex@pic.com"
        } 

    token = user_token
    client.post(
            '/api/v1/auth/signup',
            json=user,
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token))
