from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[str] = Field(
        default=None,
        alias="_id",  # Se verá como _id en Swagger/Postman
        title="ID del usuario",
        description="Identificador único del usuario (MongoDB _id)"
    )
    name: str
    email: str
    password: str