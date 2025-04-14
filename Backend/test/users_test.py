import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    payload = {
        "name": "Test User 1",
        "email": "testuser@example.com",
        "password": "secure123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == payload["name"]
    assert json_data["email"] == payload["email"]
    assert "_id" in json_data

def test_find_all_users():
    response = client.get("/users/")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    print("Number of users:", len(json_data))
    print("test_find_all_users passed")

def test_find_user_by_id():
    response = client.get("/users/67f4b3283e94b228867d7e2c")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, dict)
    assert "_id" in json_data
    print("User found:", json_data)
    print("test_find_user_by_id passed")

def test_find_user_by_id_not_found():
    response = client.get("/users/invalid_id")
    assert response.status_code == 404
    json_data = response.json()
    print("User not found test passed")

def test_update_user():
    user_id = "67f4b3283e94b228867d7e2c"
    updated_data = {
        "name": "Updated User",
        "email": "updated@example.com",
        "password": "newpass123"
    }
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]
    print("User updated test passed")

def test_delete_user():
    user_id = "67f4b3283e94b228867d7e2c"
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    print("User deleted test passed")
    

if __name__ == "__main__":
    #test_create_user()
    #test_find_all_users()
    #test_find_user_by_id()
    #test_find_user_by_id_not_found()
    #test_update_user()
    #test_delete_user()
    print("Test passed!")

