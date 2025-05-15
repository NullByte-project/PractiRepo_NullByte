from bson import ObjectId
from fastapi import HTTPException
from config.db import db
from config.jwt_manager import encode_jwt
from schemas.user_schema import TokenResponse, UserCreate, UserLogin, userEntity, usersEntity, UserPublic
from models.user_models import User
from passlib.hash import sha256_crypt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

async def register_user_controller(data: UserCreate) -> UserPublic:
    existing = await db.user.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user_dict = data.dict()

    user_dict["password"] = sha256_crypt.hash(user_dict["password"])

    user_dict["role_id"] = ObjectId(user_dict["role_id"])  
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
