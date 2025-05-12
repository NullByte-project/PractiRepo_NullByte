from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from utils.mongo_objectid import PyObjectId  # Import ObjectId from bson

from enum import Enum

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password: str
    role_id: PyObjectId

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
        },
    }


