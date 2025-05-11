from pydantic import BaseModel, Field
from typing import List, Optional
from utils.mongo_objectid import PyObjectId

class RoleCreate(BaseModel):
    name: str
    permissions: List[str] = []

class RolePublic(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    permissions: List[str] = []

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: str
        }
    }