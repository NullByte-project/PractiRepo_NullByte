import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_id07_cp01_send_contact_form():
    payload = {
        "nombre": "jose",
        "apellidos": "marquez",
        "email": "jose@example.com",
        "telefono": "Este es un telefono",
        "mensaje": "este es un mensaje",
        "tipoUsuario": "student",
        "terminos": True
    }

    response = client.post("/email/contact", json=payload)
    print("Response:", response.json())

    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"
    assert "message_id" in response.json()
    print("✅ ID07-CP-01 passed: consulta enviada correctamente.")

def test_id07_cp02_missing_fields_in_contact_form():
    # ⚠️ Falta el campo "mensaje" y "terminos"
    payload = {
        "nombre": "Ana",
        "apellidos": "Gómez",
        "email": "ana@example.com",
        "telefono": "3210001122",
        "tipoUsuario": "student"
    }

    response = client.post("/email/contact", json=payload)
    print("Response:", response.json())

    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()
    print("✅ ID07-CP-02 passed: error por campos obligatorios omitidos.")


if __name__ == "__main__":
    #test_id07_cp01_send_contact_form()
    test_id07_cp02_missing_fields_in_contact_form()
