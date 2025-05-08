import io
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_practice():
    file_data = io.BytesIO(b"%PDF-1.4 sample pdf content")
    response = client.post(
        "/practices/",
        files={"file": ("test.pdf", file_data, "application/pdf")},
        data={
            "title": "Informe prueba",
            "year": 2023,
            "practice_type": "Informes de práctica institucional II",
            "institution": "UNAL",
            "author": "Samuel",
            "municipality": "Manizales",
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Informe prueba"
    print("Practice created successfully:", response.json())
    print("test_create_practice passed")

def test_create_practice_invalid_file():
    invalid_file = io.BytesIO(b"invalid content")
    response = client.post(
        "/practices/",
        files={"file": ("file.txt", invalid_file, "text/plain")},
        data={
            "title": "Informe prueba",
            "year": 2023,
            "practice_type": "Informes de práctica institucional II",
            "institution": "UNAL",
            "author": "Samuel",
            "municipality": "Manizales",
        }  
    )
    assert response.status_code == 400
    print("Invalid file test passed")

def test_list_all_practices():
    response = client.get("/practices/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("Number of practices:", len(response.json()))
    print("test_list_all_practices passed")

def test_get_practice_by_id():
    practice_id = "67f71902d6324b57ae758b13"  # 🔁 Reemplaza con un ID válido
    response = client.get(f"/practices/{practice_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    print("Practice found:", response.json())
    print("test_get_practice_by_id passed")

def test_update_practice_with_file():
    practice_id = "67f71902d6324b57ae758b13"  # 🔁 Reemplaza con un ID válido
    with open("uploads/1744247042.pdf", "rb") as f:
        response = client.put(
            f"/practices/{practice_id}",
            files={"file": ("test.pdf", f, "application/pdf")},
            data={
                "title": "Updated Practice",
                "year": 2023,
                "practice_type": "Informes de proyectos de vida familiar y comunitaria III",
                "institution": "Updated Institution",
                "author": "Updated Author",
                "municipality": "Updated Municipality",
            }
        )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Practice"
    print("Practice updated successfully:", response.json())
    print("test_update_practice_with_file passed")



if __name__ == "__main__":
    #test_create_practice()
    #test_create_practice_invalid_file()
    #test_list_all_practices()
    #test_get_practice_by_id()
    test_update_practice_with_file()
    print("Test passed!")



