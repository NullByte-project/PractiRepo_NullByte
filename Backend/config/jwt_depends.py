from bson import ObjectId
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from config.db import db
from config.jwt_manager import decode_jwt  # asegúrate que esta función decodifique bien
from typing import List

from schemas.user_schema import UserPublic

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        payload = decode_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(status_code=403, detail="Token inválido")
        return payload

def has_permission(required: str):
    async def permission_dependency(payload: dict = Depends(JWTBearer())):
        if required not in payload.get("permissions", []):
            raise HTTPException(status_code=403, detail="Permiso insuficiente")
        print(f"Token válido con permisos: {payload.get('permissions')}")
        print(payload)
        return payload
    return permission_dependency

# --- Obtener el usuario actual a partir del token ---
async def get_current_user(payload: dict = Depends(JWTBearer())) -> UserPublic:
    email = payload.get("sub")  # El sub es el email
    print(f"Email extraído del token: {email}")

    print(f"Token válido con permisos: {payload.get('permissions')}")
    print(payload)

    if not email:
        raise HTTPException(status_code=403, detail="Token inválido: no se encontró el correo")

    user_data = await db.user.find_one({"email": email})
    print(f"Usuario encontrado: {user_data}")
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UserPublic(
        id=str(user_data["_id"]),
        name=user_data.get("name"),
        email=user_data.get("email"),
        role_id=str(user_data.get("role_id")) if user_data.get("role_id") else None
    )
# --- Validar si el usuario tiene rol 'admin' en base de datos ---
async def get_current_admin_user(current_user: UserPublic = Depends(get_current_user)) -> UserPublic:
    if not current_user.role_id:
        raise HTTPException(status_code=403, detail="Permisos insuficientes: sin rol asignado")

    role = await db.roles.find_one({"_id": ObjectId(current_user.role_id)})
    if not role or role.get("name") != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes: se requiere rol de administrador")

    return current_user