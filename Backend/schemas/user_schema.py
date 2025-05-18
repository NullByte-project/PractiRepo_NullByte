from pydantic import BaseModel, EmailStr
from typing import Optional, List
from bson import ObjectId

# Convierte un documento de usuario de la base de datos en un diccionario serializable
def userEntity(user) -> dict:
     return {
            "id": str(user["_id"]) if isinstance(user["_id"], ObjectId) else user["_id"],
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "role_id": str(user.get("role_id")) if user.get("role_id") else None
        }

# Aplica userEntity a una lista de documentos de usuarios
def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

# Esquema para login de usuario
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para creación de nuevo usuario
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: str

# Esquema para representar públicamente a un usuario (respuesta al cliente)
class UserPublic(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr
    role_id: Optional[str]

# Esquema para el registro de un nuevo usuario con nombres separados
class UserRegistrationInput(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: str

# Esquema para solicitud de cambio de contraseña
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

# Esquema para solicitud de restablecimiento de contraseña
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Esquema para la respuesta del token de autenticación
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

