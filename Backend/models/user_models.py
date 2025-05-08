from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class User(BaseModel):
    id: Optional[str] = Field(
        default=None,
        alias="_id",  
        title="ID del usuario",
        description="Identificador único del usuario (MongoDB _id)"
    )
    name: str
    email: str
    password: str
    role: UserRole = UserRole.USER
    
    
class Config:
        use_enum_values = True # Para que en la base de datos se guarde 'admin' o 'user'