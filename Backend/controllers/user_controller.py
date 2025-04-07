from bson import ObjectId
from fastapi import HTTPException
from config.db import db
from schemas.user_schema import userEntity, usersEntity
from models.user_models import User
from passlib.hash import sha256_crypt

async def find_all_users_controller():
    users_cursor = db.user.find()
    users = await users_cursor.to_list(length=100)
    return usersEntity(users)

async def create_user_controller(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.hash(new_user["password"])

    custom_id = new_user.pop("id", None)
    new_user["_id"] = custom_id if custom_id else str(ObjectId())

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