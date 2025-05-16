from bson import ObjectId
from fastapi import HTTPException
from config.db import db
from config.jwt_manager import encode_jwt
from controllers.emailController import send_email_controller
from schemas.user_schema import PasswordChangeRequest, PasswordResetRequest, TokenResponse, UserCreate, UserLogin, UserRegistrationInput, userEntity, usersEntity, UserPublic
from models.user_models import User
from passlib.hash import sha256_crypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from utils.password_generator import generate_random_password

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def find_all_users_controller():
    users_cursor = db.user.find()
    users = await users_cursor.to_list(length=100)
    return [
        UserPublic(
            id=str(u["_id"]),
            name=u.get("name", ""),
            email=u.get("email", ""),
            role_id=str(u.get("role_id")) if u.get("role_id") else "Sin rol"
        )
        for u in users
    ]

async def find_user_controller(id: str) -> UserPublic:
    print(f"ID recibido: {id}")
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    user_data = await db.user.find_one({"_id": object_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UserPublic(
        id=str(user_data["_id"]),
        name=user_data["name"],
        email=user_data["email"],
        role_id=str(user_data.get("role_id")) if user_data.get("role_id") else None
    )

async def update_user_controller(id: str, user: UserCreate) -> UserPublic:
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    updated_user = dict(user)
    updated_user["password"] = sha256_crypt.hash(updated_user["password"])

    result = await db.user.update_one({"_id": object_id}, {"$set": updated_user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_updated = await db.user.find_one({"_id": object_id})
    
    # Usa userEntity para filtrar correctamente los campos, y lo pasas a UserPublic
    user_dict = userEntity(user_updated)
    return UserPublic(**user_dict)

async def delete_user_controller(id: str):
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await db.user.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return True

#Metodos personalizados

async def get_user_by_email(email: str):
    return await db.user.find_one({"email": email})

def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return sha256_crypt.verify(plain, hashed)

async def register_user_controller(data: UserRegistrationInput) -> UserPublic:
    # Verificar duplicados
    existing = await db.user.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Unir nombre + apellido
    full_name = f"{data.first_name.strip()} {data.last_name.strip()}"

    # Convertir al esquema real de creación
    user_to_create = UserCreate(
        name=full_name,
        email=data.email,
        password=data.password,
        role_id=data.role_id
    )

    # Reutiliza tu lógica ya existente
    hashed_password = sha256_crypt.hash(user_to_create.password)
    user_dict = {
        "name": user_to_create.name,
        "email": user_to_create.email,
        "password": hashed_password,
        "role_id": ObjectId(user_to_create.role_id)
    }

    result = await db.user.insert_one(user_dict)
    saved = await db.user.find_one({"_id": result.inserted_id})

    return UserPublic(
        id=str(saved["_id"]),
        name=saved["name"],
        email=saved["email"],
        role_id=str(saved["role_id"])
    )

async def login_user_controller(user: UserLogin) -> TokenResponse:
    db_user = await db.user.find_one({"email": user.email})
    if not db_user or not sha256_crypt.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    role = await db.roles.find_one({"_id": db_user["role_id"]})
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    payload = {
        "sub": db_user["email"],
        "role_id": str(db_user["role_id"]),
        "role": role["name"],
        "permissions": role["permissions"]
    }

    token = encode_jwt(payload)
    return TokenResponse(access_token=token)

# Cambiar contraseña autenticado
async def change_password_controller(user_email: str, data: PasswordChangeRequest):
    user = await db.user.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(data.current_password, user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

    new_hashed = hash_password(data.new_password)
    await db.user.update_one({"email": user_email}, {"$set": {"password": new_hashed}})
    return {"status": "ok", "message": "Contraseña actualizada correctamente"}

async def reset_password_controller(request: PasswordResetRequest):
    user = await db.user.find_one({"email": request.email})

    # Responder siempre lo mismo, exista o no el usuario, para evitar filtración de emails
    generic_response = {
        "status": "ok",
        "message": "Si el correo está registrado, recibirás una nueva contraseña temporal."
    }

    if not user:
        return generic_response

    new_password = generate_random_password()
    hashed = hash_password(new_password)

    await db.user.update_one({"email": request.email}, {"$set": {"password": hashed}})

    html_content = f"""
    <h3>Recuperación de contraseña</h3>
    <p>Tu nueva contraseña temporal es: <strong>{new_password}</strong></p>
    <p>Por favor inicia sesión y cámbiala lo antes posible.</p>
    """

    try:
        await send_email_controller(
            to_email=request.email,
            subject="Recuperación de contraseña - PractiRepo",
            html_content=html_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")

    return generic_response


