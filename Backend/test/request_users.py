import sys
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Cargar variables del entorno
load_dotenv()

# Agregar el path del proyecto para importar 'main'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
client = TestClient(app)

# Tokens desde .env
user_token = os.getenv("USER_TOKEN_TEST")
admin_token = os.getenv("ADMIN_TOKEN_TEST")

def test_id04_cp01_create_request():
    practice_id = "68279717e46f2880908ac9c4"

    client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    response = client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 201
    print("✅ ID04-CP-01 passed")


def test_id04_cp02_duplicate_request():
    practice_id = "68279717e46f2880908ac9c4"

    response = client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 400
    print("✅ ID04-CP-02 passed")


def test_id04_cp03_approve_request():
    request_id = "6827d1d39b20ed2a1add5183"

    payload = {
        "status": "approved",
        "admin_notes": "Aprovado"
    }

    response = client.put(
        f"/document-requests/admin/manage/{request_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    print("✅ ID04-CP-03 passed")


def test_id04_cp04_reject_request():
    request_id = "6827cb39c3008b14a252454a"

    payload = {
        "status": "rejected",
        "admin_notes": "El documento no cumple requisitos"
    }

    response = client.put(
        f"/document-requests/admin/manage/{request_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
    assert "admin_notes" in response.json()
    print("✅ ID04-CP-04 passed")


def test_id04_cp05_download_without_approval():
    practice_id = "68278aa47c8602e0fec7b504"

    response = client.get(
        f"/practices/{practice_id}/download",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 403
    assert "no tienes una solicitud aprobada" in response.json()["detail"].lower()
    print("✅ ID04-CP-05 passed")


if __name__ == "__main__":
    #test_id04_cp01_create_request()
    #test_id04_cp02_duplicate_request()
    #test_id04_cp03_approve_request()
    #test_id04_cp04_reject_request()
    #test_id04_cp05_download_without_approval()
    print("Todos los casos ID04 ejecutados correctamente.")
