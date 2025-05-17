from bson import ObjectId
from fastapi import HTTPException
from config.db import db
from config.jwt_manager import encode_jwt
from controllers.emailController import send_email_controller
from schemas.user_schema import (
    PasswordChangeRequest,
    PasswordResetRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRegistrationInput,
    userEntity,
    usersEntity,
    UserPublic,
)
from models.user_models import User
from passlib.hash import sha256_crypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from utils.password_generator import generate_random_password

# Contexto para manejo de hashing de contraseñas
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# pwd_context alternativo usando bcrypt (comentado)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def find_all_users_controller():
    """
    Obtiene una lista de hasta 100 usuarios públicos desde la base de datos.
    """
    users_cursor = db.user.find()
    users = await users_cursor.to_list(length=100)

    return [
        UserPublic(
            id=str(u["_id"]),
            name=u.get("name", ""),
            email=u.get("email", ""),
            role_id=str(u.get("role_id")) if u.get("role_id") else "Sin rol",
        )
        for u in users
    ]

async def find_user_controller(id: str) -> UserPublic:
    """
    Busca un usuario por ID y devuelve su información pública.
    """
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
        role_id=str(user_data.get("role_id")) if user_data.get("role_id") else None,
    )

async def update_user_controller(id: str, user: UserCreate) -> UserPublic:
    """
    Actualiza un usuario existente con los datos proporcionados y retorna el usuario actualizado.
    """
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    updated_user = dict(user)
    # Hashea la nueva contraseña antes de actualizar
    updated_user["password"] = sha256_crypt.hash(updated_user["password"])

    result = await db.user.update_one({"_id": object_id}, {"$set": updated_user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_updated = await db.user.find_one({"_id": object_id})

    # Convierte a entidad filtrada y luego a esquema público
    user_dict = userEntity(user_updated)
    return UserPublic(**user_dict)

async def delete_user_controller(id: str):
    """
    Elimina un usuario identificado por ID.
    """
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await db.user.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return True

# Métodos personalizados para operaciones específicas

async def get_user_by_email(email: str):
    """
    Obtiene un usuario por su correo electrónico.
    """
    return await db.user.find_one({"email": email})

def hash_password(password: str) -> str:
    """
    Hashea una contraseña en texto plano.
    """
    return sha256_crypt.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash almacenado.
    """
    return sha256_crypt.verify(plain, hashed)

async def register_user_controller(data: UserRegistrationInput) -> UserPublic:
    """
    Registra un nuevo usuario, asegurándose que el email no esté duplicado.
    """
    # Verificar si ya existe el email
    existing = await db.user.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Concatenar nombre y apellido
    full_name = f"{data.first_name.strip()} {data.last_name.strip()}"

    # Construir el objeto de creación de usuario
    user_to_create = UserCreate(
        name=full_name,
        email=data.email,
        password=data.password,
        role_id=data.role_id,
    )

    # Hashear la contraseña y preparar el diccionario para la DB
    hashed_password = sha256_crypt.hash(user_to_create.password)
    user_dict = {
        "name": user_to_create.name,
        "email": user_to_create.email,
        "password": hashed_password,
        "role_id": ObjectId(user_to_create.role_id),
    }

    # Insertar en la base de datos
    result = await db.user.insert_one(user_dict)
    saved = await db.user.find_one({"_id": result.inserted_id})

    return UserPublic(
        id=str(saved["_id"]),
        name=saved["name"],
        email=saved["email"],
        role_id=str(saved["role_id"]),
    )

async def login_user_controller(user: UserLogin) -> TokenResponse:
    """
    Verifica credenciales y genera un token JWT con los permisos del usuario.
    """
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
        "permissions": role["permissions"],
    }

    token = encode_jwt(payload)
    return TokenResponse(access_token=token)

async def change_password_controller(user_email: str, data: PasswordChangeRequest):
    """
    Cambia la contraseña de un usuario autenticado, verificando la contraseña actual.
    """
    user = await db.user.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(data.current_password, user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña actual incorrecta")

    new_hashed = hash_password(data.new_password)
    await db.user.update_one({"email": user_email}, {"$set": {"password": new_hashed}})
    return {"status": "ok", "message": "Contraseña actualizada correctamente"}

async def reset_password_controller(request: PasswordResetRequest):
    """
    Genera una nueva contraseña temporal para un usuario y envía un correo con la nueva contraseña.
    Responde de manera genérica para evitar filtrar si el email existe o no.
    """
    user = await db.user.find_one({"email": request.email})

    generic_response = {
        "status": "ok",
        "message": "Si el correo está registrado, recibirás una nueva contraseña temporal.",
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
            html_content=html_content,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")

    return generic_response


