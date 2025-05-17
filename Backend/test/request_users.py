import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_id04_cp01_create_request():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlcmxleWNhYnJlcmEwNjJAZ21haWwuY29tIiwicm9sZV9pZCI6IjY4MjAyZTA0M2NkYzRjMTQxYTMwYzBmNSIsInJvbGUiOiJzdHVkZW50IiwicGVybWlzc2lvbnMiOlsicmVhZCIsInJlcXVlc3RfZG93bmxvYWQiXSwiZXhwIjoxNzQ3NDQxNDY0fQ.uBoByZafNIcFPp84XIfgAFDbBij0HvwMnDv_Hv7uR-o"
    practice_id = "68279717e46f2880908ac9c4"
    
    # Primera solicitud
    client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Segunda solicitud duplicada
    response = client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 201
    print("ID04-CP-01 passed")

def test_id04_cp02_duplicate_request():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlcmxleWNhYnJlcmEwNjJAZ21haWwuY29tIiwicm9sZV9pZCI6IjY4MjAyZTA0M2NkYzRjMTQxYTMwYzBmNSIsInJvbGUiOiJzdHVkZW50IiwicGVybWlzc2lvbnMiOlsicmVhZCIsInJlcXVlc3RfZG93bmxvYWQiXSwiZXhwIjoxNzQ3NDQxNDY0fQ.uBoByZafNIcFPp84XIfgAFDbBij0HvwMnDv_Hv7uR-o"
    practice_id = "68279717e46f2880908ac9c4"

    # Segunda solicitud duplicada
    response = client.post(
        f"/document-requests/request/{practice_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    #print("Response:", response.json())
    assert response.status_code == 400
    print("ID04-CP-02 passed")

def test_id04_cp03_approve_request():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NDQ0Nzk0fQ.-9lIkQ1cH-bjLkApdiYdaeNEI1h5Hu7e0eRUV9C7Xew"  # Reemplaza con un token de admin válido
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
    print("ID04-CP-03 passed")

def test_id04_cp04_reject_request():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NDkxOTgwfQ.XZ0wuBG9lE-GFFkgXOp0IsEwhki0xgbskGc1m7R66sE"
    request_id = "6827cb39c3008b14a252454a"  # 🛠️ Reemplaza con ID válido de solicitud pendiente

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
    print("ID04-CP-04 passed")

def test_id04_cp05_download_without_approval():
    user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlcmxleWNhYnJlcmEwNjJAZ21haWwuY29tIiwicm9sZV9pZCI6IjY4MjAyZTA0M2NkYzRjMTQxYTMwYzBmNSIsInJvbGUiOiJzdHVkZW50IiwicGVybWlzc2lvbnMiOlsicmVhZCIsInJlcXVlc3RfZG93bmxvYWQiXSwiZXhwIjoxNzQ3NDk0MzMxfQ.BfaUXLRO-oLopJ9MyGn2L8_95lEWUQ_nQuRpFWKvnS8"  # 🔁 Reemplazar con un token de un usuario autenticado SIN solicitud aprobada
    practice_id = "68278aa47c8602e0fec7b504"  # 🔁 Reemplazar con un ID de práctica para la cual no hay solicitud aprobada

    response = client.get(
        f"/practices/{practice_id}/download",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    print("Response:", response.json())
    assert response.status_code == 403
    assert "no tienes una solicitud aprobada" in response.json()["detail"].lower()
    print("ID04-CP-05 passed")



if __name__ == "__main__":
    #test_id04_cp01_create_request()
    #test_id04_cp02_duplicate_request()
    #test_id04_cp03_approve_request()
    #test_id04_cp04_reject_request()
    test_id04_cp05_download_without_approval()
    # test_id04_cp06_admin_download()
    print("Todos los casos ID04 ejecutados correctamente.")