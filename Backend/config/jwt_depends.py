from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from config.jwt_manager import decode_jwt  # asegúrate que esta función decodifique bien
from typing import List

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
        return payload
    return permission_dependency
