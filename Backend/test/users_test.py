import sys
import os

# Agrega el directorio padre al sys.path para poder importar 'main'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Variables desde el entorno
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN_TEST")
USER_TOKEN = os.getenv("USER_TOKEN_TEST")
ROLE_ID = os.getenv("DEFAULT_ROLE_ID_TEST")

def test_create_user_by_admin():
    """Crea un nuevo usuario como administrador"""
    payload = {
        "name": "Nuevo Usuario de Prueba",
        "email": "nuevo_user@example.com",
        "password": "test1234",
        "role_id": ROLE_ID
    }

    response = client.post(
        "/users/admin/create",
        headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
        json=payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert "id" in data
    print("✅ Usuario creado por admin:", data["id"])


def test_get_all_users():
    """Consulta todos los usuarios"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ Lista de usuarios obtenida")


def test_get_user_profile():
    """Consulta el perfil del usuario autenticado"""
    response = client.get("/users/mi-perfil", headers={"Authorization": f"Bearer {USER_TOKEN}"})
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    print("✅ Perfil de usuario obtenido:", data["email"])


def test_update_user_by_id():
    """Actualiza los datos de un usuario (admin)"""
    user_id = "REEMPLAZAR_ID"  # Coloca aquí un ID válido manualmente o desde test previo
    updated = {
        "name": "Usuario Actualizado",
        "email": "actualizado@example.com",
        "password": "nuevaClave123",
        "role_id": ROLE_ID
    }

    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
        json=updated
    )
    assert response.status_code == 200
    assert response.json()["email"] == updated["email"]
    print("✅ Usuario actualizado:", response.json()["email"])


def test_delete_user_by_id():
    """Elimina un usuario existente (admin)"""
    user_id = "REEMPLAZAR_ID"  # Coloca aquí un ID válido manualmente o desde test previo

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
    )
    assert response.status_code in [204, 404]
    print("✅ Usuario eliminado (o no encontrado):", user_id)


def test_protected_download_permission():
    """Valida que un usuario sin permiso recibe error"""
    response = client.get(
        "/users/descargar",
        headers={"Authorization": f"Bearer {USER_TOKEN}"}
    )
    assert response.status_code == 403
    print("✅ Acceso denegado correctamente por permisos insuficientes")


if __name__ == "__main__":
    #test_create_user_by_admin()
    #test_get_all_users()
    #test_get_user_profile()
    test_protected_download_permission()
    # test_update_user_by_id()
    # test_delete_user_by_id()