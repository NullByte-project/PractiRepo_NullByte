from pydantic import BaseModel, Field
from typing import List, Optional
from utils.mongo_objectid import PyObjectId

# Esquema para crear un nuevo rol
class RoleCreate(BaseModel):
    name: str  # Nombre del rol
    permissions: List[str] = []  # Lista de permisos asignados al rol

# Esquema público para representar un rol (respuesta)
class RolePublic(BaseModel):
    id: Optional[str] = Field(alias="_id")  # ID del rol, mapeado desde '_id' de MongoDB
    name: str  # Nombre del rol
    permissions: List[str] = []  # Permisos asignados al rol

    model_config = {
        "populate_by_name": True,  # Permite usar '_id' en datos y acceder como 'id' en el modelo
        "arbitrary_types_allowed": True,  # Habilita tipos personalizados como PyObjectId
        "json_encoders": {
            PyObjectId: str  # Convierte PyObjectId a string en las respuestas JSON
        }
    }
