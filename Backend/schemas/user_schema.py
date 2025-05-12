from pydantic import BaseModel, EmailStr
from typing import Optional, List
from bson import ObjectId
def userEntity(user) -> dict:
     return {
            "id": str(user["_id"]) if isinstance(user["_id"], ObjectId) else user["_id"],
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "role_id": str(user.get("role_id")) if user.get("role_id") else None
        }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: str

class UserPublic(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr
    role_id: Optional[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
