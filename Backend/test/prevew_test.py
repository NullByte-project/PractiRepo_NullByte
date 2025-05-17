import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_preview_success():
    
    practice_id = "67f3f2808a605323a584cfe0" 

    # 2. Generar previsualización
    preview_response = client.get(f"/previews/{practice_id}")
    assert preview_response.status_code == 200
    fragments = preview_response.json()
    print(fragments)
    assert isinstance(fragments, list)
    assert all("content" in frag for frag in fragments)
    assert all("page_number" in frag for frag in fragments)
    print("test_generate_preview passed")

def test_id06_cp01_public_access_to_preview():
    practice_id = "68278aec7c8602e0fec7b506"  # 🔁 Reemplaza con un ID válido con previsualización generada

    response = client.get(f"/previews/{practice_id}")

    preview_data = response.json()
    print("Response:", preview_data)

    assert response.status_code == 200
    assert isinstance(preview_data, list)
    assert len(preview_data) > 0
    assert all("content" in page and "page_number" in page for page in preview_data)
    
    print("✅ ID06-CP-01 passed: acceso público a previsualización permitido.")

def test_id06_cp02_upload_invalid_format():
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NTA2NDg1fQ.AIMxjDtj_6iScE_cUlrDUWunv1eYBRdkbj6dzHX8S5I"
    
    invalid_file = io.BytesIO(b"This is not a valid PDF content")
    
    response = client.post(
        "/practices/",
        headers={"Authorization": f"Bearer {admin_token}"},
        files={"file": ("test.txt", invalid_file, "text/plain")},
        data={
            "title": "Práctica Inválida",
            "year": 2025,
            "practice_type": "Informes de práctica institucional II",
            "institution": "UNAL",
            "author": "Admin Test",
            "municipality": "Bogotá"
        }
    )

    print("Response:", response.json())
    detail = response.json()["detail"].lower()
    assert response.status_code == 400
    assert "formato de archivo no permitido" in detail or "formato no permitido" in detail
    print("✅ ID06-CP-02 passed: bloqueo correcto para archivo no permitido.")

def test_id06_cp03_admin_upload_pdf_generates_preview():
    import io
    admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzcGVyYW10b0BtYWlsLmNvbSIsInJvbGVfaWQiOiI2ODIwMmRlMzNjZGM0YzE0MWEzMGMwZjQiLCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGUiLCJyZWFkIiwidXBkYXRlIiwiZGVsZXRlIiwiYXBwcm92ZV9kb3dubG9hZHMiXSwiZXhwIjoxNzQ3NTEwOTU2fQ.Vngf96Xiqsv_snoEdJxocAF98fAhvwh7ToBq6OU4zoI"  # tu token real

    # PDF válido mínimo
    minimal_valid_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog >>\nendobj\n"
        b"xref\n0 1\n0000000000 65535 f \n"
        b"trailer\n<< /Root 1 0 R >>\nstartxref\n0\n%%EOF"
    )
    file_data = io.BytesIO(minimal_valid_pdf)

    response = client.post(
        "/practices/",
        headers={"Authorization": f"Bearer {admin_token}"},
        files={"file": ("test.pdf", file_data, "application/pdf")},
        data={
            "title": "Documento Actualizado de Prueba 3",
            "year": 2025,
            "practice_type": "Informes de práctica institucional II",
            "institution": "UNAL",
            "author": "Admin Tester",
            "municipality": "Medellín"
        }
    )

    print("Response:", response.json())
    assert response.status_code == 201
    assert "id" in response.json()
    

    print("✅ ID06-CP-03 passed: documento PDF válido cargado y mini-PDF generado.")

if __name__ == "__main__":
    #test_id06_cp01_public_access_to_preview()
    #test_id06_cp02_upload_invalid_format()
    test_id06_cp03_admin_upload_pdf_generates_preview()
