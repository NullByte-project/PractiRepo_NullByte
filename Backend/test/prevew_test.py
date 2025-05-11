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

if __name__ == "__main__":
    test_generate_preview_success()
