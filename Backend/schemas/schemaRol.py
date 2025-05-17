from pydantic import BaseModel, Field
from typing import Optional, List

# Esquema para la creación de un nuevo rol
class RoleCreate(BaseModel):
    name: str  # Nombre del rol
    permissions: Optional[List[str]] = []  # Lista opcional de permisos asignados al rol
    description: Optional[str] = None  # Descripción opcional del rol

# Esquema para representar públicamente un rol (por ejemplo, en respuestas de API)
class RolePublic(BaseModel):
    id: Optional[str]  # ID único del rol
    name: str  # Nombre del rol
    permissions: List[str] = []  # Lista de permisos del rol
    description: Optional[str] = None  # Descripción opcional del rol
