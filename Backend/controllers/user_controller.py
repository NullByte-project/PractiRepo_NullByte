from bson import ObjectId
from fastapi import HTTPException
from config.db import db
from schemas.user_schema import userEntity, usersEntity
from models.user_models import User
from passlib.hash import sha256_crypt

def find_all_users_controller():
    return usersEntity(db.user.find())

def create_user_controller(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.hash(new_user["password"])

    # Obtener id enviado o generar uno
    custom_id = new_user.pop("id", None)
    new_user["_id"] = custom_id if custom_id else str(ObjectId())

    # Verificar si ya existe ese _id en la base
    if db.user.find_one({"_id": new_user["_id"]}):
        # Si ya existe, reemplazar con uno nuevo automáticamente
        new_user["_id"] = str(ObjectId())

    # Insertar usuario
    inserted_id = db.user.insert_one(new_user).inserted_id
    created_user = db.user.find_one({"_id": inserted_id})
    return userEntity(created_user)


# def create_user_controller(user: User):
#     new_user = dict(user)
#     new_user["password"] = sha256_crypt.hash(new_user["password"])
#     new_user["_id"] = new_user.pop("id", None) or str(ObjectId())

#     # Verificar si ya existe un usuario con ese _id
#     if db.user.find_one({"_id": new_user["_id"]}):
#         raise HTTPException(status_code=400, detail=f"El ID '{new_user['_id']}' ya está en uso.")

#     # Verificar si ya existe un usuario con ese email
#     if db.user.find_one({"email": new_user["email"]}):
#         raise HTTPException(status_code=400, detail="El correo ya está registrado.")

#     inserted_id = db.user.insert_one(new_user).inserted_id
#     created_user = db.user.find_one({"_id": inserted_id})
#     return userEntity(created_user)


def find_user_controller(id: str):
    user_data = db.user.find_one({"_id": id})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return userEntity(user_data)


def update_user_controller(id: str, user: User):
    updated_user = dict(user)
    updated_user.pop("id", None)
    updated_user["password"] = sha256_crypt.hash(updated_user["password"])

    result = db.user.update_one({"_id": id}, {"$set": updated_user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return userEntity(db.user.find_one({"_id": id}))


def delete_user_controller(id: str):
    result = db.user.delete_one({"_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return True