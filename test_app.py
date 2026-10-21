import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_send_message_json(client):
    response = client.post('/api/send-message', json={
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message."
    })
    assert response.status_code == 200

def test_send_message_form(client):
    response = client.post('/api/send-message', data={
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message."
    })
    assert response.status_code == 415
