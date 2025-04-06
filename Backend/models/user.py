from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    _id: Optional[str]  # Ahora se usa directamente "_id"
    name: str
    email: str          # Email como string simple
    password: str