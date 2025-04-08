import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "name": "Tester",
        "email": "tester@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
