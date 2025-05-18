# models/documentRequestModel.py
from config.db import db
from bson import ObjectId  # Importar ObjectId directamente de bson para manejar IDs MongoDB
from typing import List, Dict, Any, Optional
from datetime import datetime
from schemas.schemaDocumentRequest import DocumentRequestStatus

# Referencia a las colecciones relacionadas en la base de datos
practices_collection = db["practices"]
users_collection = db["user"]


class DocumentRequestModel:
    collection = db["document_requests"]

    @classmethod
    async def create(cls, practice_id: str, user_id: str) -> str:
        """
        Crea una nueva solicitud de descarga para la práctica y usuario indicados.
        Valida que los IDs sean válidos y guarda la solicitud con estado pendiente.
        Retorna el ID de la nueva solicitud como string.
        """
        try:
            practice_obj_id = ObjectId(practice_id)
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise ValueError("Formato inválido para practice_id o user_id")

        request_data = {
            "practice_id": practice_obj_id,
            "requested_by_id": user_obj_id,
            "request_date": datetime.utcnow(),
            "status": DocumentRequestStatus.PENDING.value
        }
        result = await cls.collection.insert_one(request_data)
        return str(result.inserted_id)

    @classmethod
    async def _enrich_request_data(cls, request_doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Método privado para enriquecer la información de una solicitud:
        - Añade título de la práctica
        - Añade email y nombre del usuario solicitante
        - Establece valores por defecto para campos opcionales
        """
        if not request_doc:
            return None

        # Obtener título de la práctica
        practice = await practices_collection.find_one({"_id": request_doc.get("practice_id")})
        request_doc["practice_title"] = practice.get("title") if practice else "Título no encontrado"

        # Obtener datos del usuario solicitante
        user_id = request_doc.get("requested_by_id")
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except Exception:
                user_id = None

        requester = await users_collection.find_one({"_id": user_id}) if user_id else None
        request_doc["requester_email"] = requester.get("email") if requester else None
        request_doc["requester_name"] = requester.get("name") if requester else "Usuario desconocido"

        # Campos opcionales con valor por defecto si no existen
        request_doc.setdefault("response_date", None)
        request_doc.setdefault("response_by_id", None)
        request_doc.setdefault("admin_notes", None)

        return request_doc

    @classmethod
    async def get_by_id_enriched(cls, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una solicitud por su ID y la devuelve con datos enriquecidos.
        Retorna None si el ID es inválido o no se encuentra la solicitud.
        """
        try:
            obj_id = ObjectId(request_id)
        except Exception:
            return None

        request = await cls.collection.find_one({"_id": obj_id})
        return await cls._enrich_request_data(request)

    @classmethod
    async def get_by_user_enriched(cls, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las solicitudes realizadas por un usuario específico,
        ordenadas por fecha de solicitud (más recientes primero) y enriquecidas.
        """
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            return []

        cursor = cls.collection.find({"requested_by_id": user_obj_id}).sort("request_date", -1)
        requests = await cursor.to_list(length=None)

        enriched_requests = []
        for req in requests:
            enriched = await cls._enrich_request_data(req)
            if enriched:
                enriched_requests.append(enriched)

        return enriched_requests

    @classmethod
    async def get_all_enriched(cls, status_filter: Optional[DocumentRequestStatus] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las solicitudes en la base de datos, opcionalmente filtradas
        por estado, ordenadas por fecha y enriquecidas con datos relacionados.
        """
        query = {}
        if status_filter:
            query["status"] = status_filter.value

        cursor = cls.collection.find(query).sort("request_date", -1)
        requests = await cursor.to_list(length=None)

        enriched_requests = []
        for req in requests:
            enriched = await cls._enrich_request_data(req)
            if enriched:
                enriched_requests.append(enriched)

        return enriched_requests

    @classmethod
    async def update_status_by_admin(
        cls,
        request_id: str,
        new_status: DocumentRequestStatus,
        admin_id: str,
        admin_notes: Optional[str] = None
    ) -> bool:
        """
        Actualiza el estado de una solicitud, junto con la fecha de respuesta,
        el ID del administrador que responde y notas administrativas opcionales.
        Retorna True si se actualizó correctamente, False si el ID no es válido o no se modificó.
        """
        try:
            obj_id = ObjectId(request_id)
            admin_obj_id = ObjectId(admin_id)
        except Exception:
            return False  # ID inválido

        update_fields = {
            "status": new_status.value,
            "response_date": datetime.utcnow(),
            "response_by_id": admin_obj_id
        }

        if admin_notes is not None:
            update_fields["admin_notes"] = admin_notes
        # Si admin_notes es None, no se incluye en $set para evitar sobrescribir datos existentes.

        result = await cls.collection.update_one({"_id": obj_id}, {"$set": update_fields})
        return result.modified_count > 0

    @classmethod
    async def find_approved_request(cls, practice_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca una solicitud aprobada para una práctica y usuario específicos.
        Retorna la solicitud si existe, None si no se encuentra o IDs inválidos.
        """
        try:
            practice_obj_id = ObjectId(practice_id)
            user_obj_id = ObjectId(user_id)
        except Exception:
            return None

        return await cls.collection.find_one({
            "practice_id": practice_obj_id,
            "requested_by_id": user_obj_id,
            "status": DocumentRequestStatus.APPROVED.value
        })

    @classmethod
    async def check_existing_request(cls, practice_id: str, user_id: str) -> bool:
        """
        Verifica si ya existe una solicitud con estado pendiente o aprobado para
        la práctica y usuario indicados.
        Retorna True si existe, False en caso contrario o si los IDs son inválidos.
        """
        try:
            practice_obj_id = ObjectId(practice_id)
            user_obj_id = ObjectId(user_id)
        except Exception:
            return False

        existing = await cls.collection.find_one({
            "practice_id": practice_obj_id,
            "requested_by_id": user_obj_id,
            "status": {"$in": [DocumentRequestStatus.PENDING.value, DocumentRequestStatus.APPROVED.value]}
        })
        return existing is not None
