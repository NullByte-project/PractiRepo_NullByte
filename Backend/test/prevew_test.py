import io
import sys
import os

from fastapi.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

# Token desde .env
admin_token = os.getenv("ADMIN_TOKEN_TEST")


def test_generate_preview_success():
    """Prueba que se genere correctamente la previsualización de una práctica"""
    practice_id = "67f3f2808a605323a584cfe0"

    preview_response = client.get(f"/previews/{practice_id}")
    assert preview_response.status_code == 200
    fragments = preview_response.json()
    print(fragments)

    assert isinstance(fragments, list)
    assert all("content" in frag for frag in fragments)
    assert all("page_number" in frag for frag in fragments)
    print("✅ test_generate_preview_success passed")


def test_id06_cp01_public_access_to_preview():
    """Prueba de acceso público a la previsualización"""
    practice_id = "68278aec7c8602e0fec7b506"

    response = client.get(f"/previews/{practice_id}")
    preview_data = response.json()
    print("Response:", preview_data)

    assert response.status_code == 200
    assert isinstance(preview_data, list)
    assert len(preview_data) > 0
    assert all("content" in page and "page_number" in page for page in preview_data)

    print("✅ ID06-CP-01 passed: acceso público permitido.")


def test_id06_cp02_upload_invalid_format():
    """Carga de archivo no válido, se espera error 400"""
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
    print("✅ ID06-CP-02 passed: archivo inválido bloqueado correctamente.")


def test_id06_cp03_admin_upload_pdf_generates_preview():
    """Carga válida de PDF y generación automática de previsualización"""
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
    print("✅ ID06-CP-03 passed: PDF válido subido y previsualización generada.")


if __name__ == "__main__":
    #test_generate_preview_success()
    #test_id06_cp01_public_access_to_preview()
    #test_id06_cp02_upload_invalid_format()
    test_id06_cp03_admin_upload_pdf_generates_preview()