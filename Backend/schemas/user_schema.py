from pydantic import BaseModel, EmailStr
from typing import Optional, List
def userEntity(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "password": item["password"],
        "role_id": str(item.get("role_id", ""))
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
    role_id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
