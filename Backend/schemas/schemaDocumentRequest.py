# schemas/schemaDocumentRequest.py
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

from utils.mongo_objectid import PyObjectId


class DocumentRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DOWNLOADED = "downloaded" # Corregido typo (era DONLOAD)


class DocumentRequestCreate(BaseModel):
    # Este schema es solo para la entrada del usuario al solicitar.
    # practice_id vendrá del Path Parameter en la ruta.
    # requested_by_id se tomará del usuario autenticado.
    pass # No necesita campos aquí si practice_id se toma del path


class DocumentRequestPublic(BaseModel):
    id: PyObjectId = Field(alias="_id", description="ID de la solicitud")
    practice_id: PyObjectId = Field(description="ID de la práctica asociada")
    practice_title: Optional[str] = Field(None, description="Título de la práctica")
    requested_by_id: PyObjectId = Field(description="ID del usuario que solicitó")
    requester_email: Optional[EmailStr] = Field(None, description="Email del solicitante")
    requester_name: Optional[str] = Field(None, description="Nombre del solicitante")
    request_date: datetime = Field(description="Fecha de la solicitud")
    status: DocumentRequestStatus = Field(description="Estado de la solicitud")
    response_date: Optional[datetime] = Field(None, description="Fecha de la respuesta del administrador")
    # Para response_by_id, Pydantic manejará ObjectId a str si el encoder está bien.
    # Si response_by_id puede ser None, Optional[PyObjectId] es correcto.
    response_by_id: Optional[PyObjectId] = Field(None, description="ID del administrador que respondió")
    admin_notes: Optional[str] = Field(None, description="Notas del administrador")

    model_config = {
        "populate_by_name": True, # Permite usar '_id' en datos y 'id' en el modelo
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: lambda oid: str(oid) if oid else None, # Manejar ObjectId y None
            ObjectId: lambda oid: str(oid) if oid else None, # Por si acaso llega un ObjectId puro
            datetime: lambda dt: dt.isoformat() if dt else None
        }
    }


class DocumentRequestUpdateAdmin(BaseModel):
    status: DocumentRequestStatus = Field(..., description="Nuevo estado (approved o rejected)")
    admin_notes: Optional[str] = Field(None, description="Notas del administrador")