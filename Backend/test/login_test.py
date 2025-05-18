import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from fastapi.testclient import TestClient
from main import app

user_token = os.getenv("USER_TOKEN_TEST")

client = TestClient(app)
def test_id08_cp01_login_valid_credentials():
    # Credenciales de un usuario registrado en la base de datos
    payload = {
        "email": "erleycabrera062@gmail.com",  # 🔁 Asegúrate de que este correo exista
        "password": "12345678"        # 🔁 Asegúrate de que la contraseña sea correcta
    }

    response = client.post("/users/login", json=payload)
    print("Response:", response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"].startswith("eyJ")  # Verificamos estructura básica de un JWT
    print("✅ ID08-CP-01 passed: inicio de sesión exitoso con credenciales válidas.")

def test_id08_cp02_login_invalid_password():
    # Datos de un usuario existente pero con contraseña incorrecta
    payload = {
        "email": "speramto@mail.com",    # 🔁 Asegúrate de que este correo exista en la DB
        "password": "wrong_password"     # ❌ Contraseña incorrecta
    }

    response = client.post("/users/login", json=payload)
    print("Response:", response.json())

    assert response.status_code == 401
    assert "Credenciales inválidas" in response.json()["detail"]
    print("✅ ID08-CP-02 passed: intento fallido de inicio de sesión con contraseña errónea correctamente detectado.")

def test_id08_cp03_reset_password_registered_email():
    # 📨 Email registrado en la base de datos
    payload = {
        "email": "erleycabrera062@gmail.com"  # 🔁 Asegúrate de que este correo exista
    }

    response = client.post("/users/reset-password", json=payload)
    print("Response:", response.json())

    assert response.status_code == 200
    assert "message" in response.json()
    assert "contraseña temporal" in response.json()["message"].lower()
    print("✅ ID08-CP-03 passed: recuperación de contraseña exitosa para correo registrado.")


def test_id08_cp04_user_changes_password():
    # 🛡️ Token JWT válido para un usuario
    
    payload = {
        "current_password": "Qdka65h1cX",   # Asegúrate que sea la actual
        "new_password": "12345678"
    }

    response = client.post(
        "/users/change-password",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())

    assert response.status_code == 200
    assert "actualizada" in response.json()["message"].lower()
    print("✅ ID08-CP-04 passed: cambio de contraseña exitoso.")



if __name__ == "__main__":
    test_id08_cp01_login_valid_credentials()
    #test_id08_cp02_login_invalid_password()
    #test_id08_cp03_reset_password_registered_email()
    #test_id08_cp04_user_changes_password()
    print("Test passed!")
