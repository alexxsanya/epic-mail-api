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