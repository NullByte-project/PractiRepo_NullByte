from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

db = conn["repositorio_practicas"]
user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(db.user.find())

@user.post('/users', response_model=User, tags=["users"])
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.hash(new_user["password"])
    new_user.pop("_id", None)

    if db.user.find_one({"email": new_user["email"]}):
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    inserted_id = db.user.insert_one(new_user).inserted_id
    created_user = db.user.find_one({"_id": inserted_id})
    return userEntity(created_user)

@user.get('/users/{id}', response_model=User, tags=["users"])
def find_user(id: str):
    user_data = db.user.find_one({"_id": ObjectId(id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return userEntity(user_data)

@user.put('/users/{id}', response_model=User, tags=["users"])
def update_user(id: str, user: User):
    updated_user = dict(user)
    updated_user.pop("_id", None)
    updated_user["password"] = sha256_crypt.hash(updated_user["password"])

    result = db.user.update_one({"_id": ObjectId(id)}, {"$set": updated_user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return userEntity(db.user.find_one({"_id": ObjectId(id)}))

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    result = db.user.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Response(status_code=HTTP_204_NO_CONTENT)