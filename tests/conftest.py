import pytest
from api import app as p

@pytest.fixture
def app():
    app = p
    return app

@pytest.fixture
def client(app):
    return app.test_client()
