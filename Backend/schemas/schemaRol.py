from pydantic import BaseModel, Field
from typing import Optional, List

class RoleCreate(BaseModel):
    name: str
    permissions: Optional[List[str]] = []
    description: Optional[str] = None

class RolePublic(BaseModel):
    id: Optional[str]
    name: str
    permissions: List[str] = []
    description: Optional[str] = None