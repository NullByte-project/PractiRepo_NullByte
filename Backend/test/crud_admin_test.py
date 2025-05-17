import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_id05_cp01_admin_creates_user():
    # 🛡️ Token JWT de un administrador (ajusta el valor real de tu token)
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NDk2MzI2fQ.W-sgMU-pMB76RkPTMZdIbM4MVtNozbwAOETFzNMGY0E"  # Reemplaza por un token válido de admin

    # 📤 Datos válidos de un nuevo usuario
    new_user_payload = {
        "name": "Carlos Ramírez",
        "email": "carlos.ramirez@example.com",
        "password": "12345678",
        "role_id": "68202e043cdc4c141a30c0f5"  # 🧩 Reemplaza con un ID de rol existente
    }

    response = client.post(
        "/users/admin/create",
        json=new_user_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["email"] == new_user_payload["email"]
    assert response.json()["name"] == "Carlos Ramírez"
    print("ID05-CP-01 passed ✅")

def test_id05_cp02_admin_create_user_with_duplicate_email():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NDk3MDk4fQ.j4aOci33AFFQX3L-fiLUvIeriRXvPxoGgoBgCCvfwAI"
    role_id = "68202e043cdc4c141a30c0f5"            # 🔁 Reemplaza por un ObjectId válido en tu base de datos

    # Paso 1: Crear usuario original (si no existe ya)
    payload = {
        "name": "Usuario Duplicado",
        "email": "duplicado@example.com",
        "password": "secure123",
        "role_id": role_id
    }

    # Paso 2: Intentar crear otro usuario con el mismo email
    response = client.post("/users/admin/create", json=payload, headers={"Authorization": f"Bearer {admin_token}"})
    
    print("Response:", response.json())
    assert response.status_code == 400
    assert "ya registrado" in response.json()["detail"]
    print("✅ ID05-CP-02 passed: intento duplicado correctamente bloqueado.")

def test_id05_cp03_user_without_admin_role_cannot_create_user():
    user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlcmxleWNhYnJlcmEwNjJAZ21haWwuY29tIiwicm9sZV9pZCI6IjY4MjAyZTA0M2NkYzRjMTQxYTMwYzBmNSIsInJvbGUiOiJzdHVkZW50IiwicGVybWlzc2lvbnMiOlsicmVhZCIsInJlcXVlc3RfZG93bmxvYWQiXSwiZXhwIjoxNzQ3NTAyMjc1fQ.nycutfTvZqevvVJLnT1hzyKtb-zb5BHsSmx72-YHwM0"

    payload = {
        "name": "Intento Ilegal",
        "email": "ilegal@example.com",
        "password": "unauthorized123",
        "role_id": "68202e043cdc4c141a30c0f5"
    }

    response = client.post(
        "/users/admin/create",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())
    assert response.status_code in [401, 403]
    print("✅ ID05-CP-03 passed: acceso denegado para usuario sin permisos de administrador")

def test_id05_cp04_admin_edits_practice():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NTA1MDM5fQ.JbT3mTkJNA6GUSAANWVM9ZhirbSpWHrRnOSJryo3EvE"
    practice_id = "68279717e46f2880908ac9c4"            # 🔁 Reemplaza por un ObjectId válido en tu base de datos
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
    print("✅ ID05-CP-04 passed: práctica editada correctamente.")



if __name__ == "__main__":
    #test_id05_cp01_admin_creates_user()
    #test_id05_cp02_admin_create_user_with_duplicate_email()
    #test_id05_cp03_user_without_admin_role_cannot_create_user()
    test_id05_cp04_admin_edits_practice()
    print("Todos los casos ID04 ejecutados correctamente.")
