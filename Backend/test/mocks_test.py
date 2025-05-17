import sys
import os
import io
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Configurar ruta y entorno
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from main import app

client = TestClient(app)

# Variables desde .env
user_token = os.getenv("USER_TOKEN_TEST")
admin_token = os.getenv("ADMIN_TOKEN_TEST")


def test_id04_cp01_create_request_mocked():
    # Resultado simulado que retornará el mock

    practice_id = "68278b1d7c8602e0fec7b507"

    fake_response = {
        "id": "mocked_id_123",
        "practice_id": practice_id,
        "requested_by_id": "mocked_user_id",
        "status": "pending"
    }

    # Usar el path real al controlador
    with patch("controllers.documentRequestController.create_document_request_controller", new=AsyncMock(return_value=fake_response)):
        response = client.post(
            f"/document-requests/request/{practice_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        print("Response:", response.json())
        assert response.status_code == 201
        assert response.json()["status"] == "pending"
        print("✅ ID04-CP-01 passed (mocked)")

def test_id07_cp01_send_contact_form_mocked():
    payload = {
        "nombre": "Ana",
        "apellidos": "Pérez",
        "email": "ana@example.com",
        "telefono": "1234567890",
        "mensaje": "Quiero más información",
        "tipoUsuario": "estudiante",
        "terminos": True
    }

    # Simular que el correo se envía correctamente
    with patch("controllers.emailController.send_email_controller", new=AsyncMock(return_value={"status": "ok", "message_id": "<fake-id@correo>"})):
        response = client.post("/email/contact", json=payload)

    print("Contact form response:", response.json())
    assert response.status_code == 200
    assert "status" in response.json()
    print("✅ ID07-CP-01 passed (mocked)")

if __name__ == "__main__":
    # test_id04_cp01_create_request_mocked()
    test_id07_cp01_send_contact_form_mocked()

    
