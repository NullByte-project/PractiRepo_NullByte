import sys
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Agrega el path del proyecto y carga variables de entorno
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from main import app

client = TestClient(app)

# ✅ Variables desde .env
admin_token = os.getenv("ADMIN_TOKEN_TEST")
user_token = os.getenv("USER_TOKEN_TEST")
role_id = os.getenv("DEFAULT_ROLE_ID_TEST", "68202e043cdc4c141a30c0f5")  # ObjectId de rol
practice_id = os.getenv("PRACTICE_ID_TEST", "68279717e46f2880908ac9c4")  # ID válido de práctica


def test_id05_cp01_admin_creates_user():
    payload = {
        "name": "Carlos Ramírez",
        "email": "carlos.ramirez@example.com",
        "password": "12345678",
        "role_id": role_id
    }

    response = client.post(
        "/users/admin/create",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]
    assert response.json()["name"] == payload["name"]
    print("✅ ID05-CP-01 passed")


def test_id05_cp02_admin_create_user_with_duplicate_email():
    payload = {
        "name": "Usuario Duplicado",
        "email": "duplicado@example.com",
        "password": "secure123",
        "role_id": role_id
    }

    # Crear el usuario si no existe
    client.post("/users/admin/create", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

    # Intentar duplicar
    response = client.post("/users/admin/create", json=payload, headers={"Authorization": f"Bearer {admin_token}"})

    print("Response:", response.json())
    assert response.status_code == 400
    assert "ya registrado" in response.json()["detail"]
    print("✅ ID05-CP-02 passed: duplicado bloqueado")


def test_id05_cp03_user_without_admin_role_cannot_create_user():
    payload = {
        "name": "Intento Ilegal",
        "email": "ilegal@example.com",
        "password": "unauthorized123",
        "role_id": role_id
    }

    response = client.post(
        "/users/admin/create",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())
    assert response.status_code in [401, 403]
    print("✅ ID05-CP-03 passed: acceso denegado sin rol admin")


def test_id05_cp04_admin_edits_practice():
    payload = {
        "title": "Práctica Actualizada",
        "year": 2025,
        "practice_type": "Informes de práctica institucional II",
        "institution": "UNAL Actualizado",
        "author": "Admin Editado",
        "municipality": "Medellín"
    }

    response = client.put(
        f"/practices/{practice_id}",
        data=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["title"] == "Práctica Actualizada"
    print("✅ ID05-CP-04 passed: práctica editada correctamente")


if __name__ == "__main__":
    test_id05_cp01_admin_creates_user()
    # test_id05_cp02_admin_create_user_with_duplicate_email()
    # test_id05_cp03_user_without_admin_role_cannot_create_user()
    # test_id05_cp04_admin_edits_practice()
