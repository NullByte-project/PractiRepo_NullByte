# schemas/schemaDocumentRequest.py

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

from utils.mongo_objectid import PyObjectId

# Enumeración de estados posibles para una solicitud de documento
class DocumentRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DOWNLOADED = "downloaded"

"""
Esquema para la creación de una solicitud de documento
No requiere campos en el cuerpo, ya que:
- El ID de la práctica se obtiene del path.
- El ID del solicitante se toma del usuario autenticado. 
"""
class DocumentRequestCreate(BaseModel):
    pass

# Esquema público para representar una solicitud de documento (respuesta)
class DocumentRequestPublic(BaseModel):
    id: PyObjectId = Field(alias="_id", description="ID de la solicitud")
    practice_id: PyObjectId = Field(description="ID de la práctica asociada")
    practice_title: Optional[str] = Field(None, description="Título de la práctica")
    requested_by_id: PyObjectId = Field(description="ID del usuario que realizó la solicitud")
    requester_email: Optional[EmailStr] = Field(None, description="Correo electrónico del solicitante")
    requester_name: Optional[str] = Field(None, description="Nombre del solicitante")
    request_date: datetime = Field(description="Fecha en que se realizó la solicitud")
    status: DocumentRequestStatus = Field(description="Estado actual de la solicitud")
    response_date: Optional[datetime] = Field(None, description="Fecha de respuesta por parte del administrador")
    response_by_id: Optional[PyObjectId] = Field(None, description="ID del administrador que respondió la solicitud")
    admin_notes: Optional[str] = Field(None, description="Notas o comentarios del administrador")

    model_config = {
        "populate_by_name": True,  # Permite usar '_id' como clave en datos entrantes y 'id' en el modelo
        "arbitrary_types_allowed": True,  # Permite el uso de tipos personalizados como PyObjectId
        "json_encoders": {
            PyObjectId: lambda oid: str(oid) if oid else None,
            ObjectId: lambda oid: str(oid) if oid else None,
            datetime: lambda dt: dt.isoformat() if dt else None
        }
    }

# Esquema utilizado por el administrador para actualizar el estado de una solicitud
class DocumentRequestUpdateAdmin(BaseModel):
    status: DocumentRequestStatus = Field(..., description="Nuevo estado de la solicitud (approved o rejected)")
    admin_notes: Optional[str] = Field(None, description="Notas opcionales del administrador respecto a la decisión")
