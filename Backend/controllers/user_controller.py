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
    return usersEntity(users)

async def create_user_controller(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.hash(new_user["password"])

    new_user.pop("id", None)
    new_user["_id"] = str(ObjectId())
    #new_user["_id"] = custom_id if custom_id else str(ObjectId())

    # Verifica duplicado
    if await db.user.find_one({"_id": new_user["_id"]}):
        new_user["_id"] = str(ObjectId())

    result = await db.user.insert_one(new_user)
    created_user = await db.user.find_one({"_id": result.inserted_id})
    return userEntity(created_user)

async def find_user_controller(id: str):
    user_data = await db.user.find_one({"_id": id})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return userEntity(user_data)

async def update_user_controller(id: str, user: User):
    updated_user = dict(user)
    updated_user.pop("id", None)
    updated_user["password"] = sha256_crypt.hash(updated_user["password"])

    result = await db.user.update_one({"_id": id}, {"$set": updated_user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_updated = await db.user.find_one({"_id": id})
    return userEntity(user_updated)

async def delete_user_controller(id: str):
    result = await db.user.delete_one({"_id": id})
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
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    user_dict["role_id"] = ObjectId(user_dict["role_id"])  # ✅ convertir a ObjectId

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
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
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
