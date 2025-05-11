from config.db import db
from bson import ObjectId
from typing import List, Dict, Any, Optional
from datetime import datetime

class DocumentRequestModel:
    colection = db["document_requests"]

    @classmethod
    async def create(cls, request_data: Dict[str, Any]) -> str:
        request_data["requestDate"] = request_data.get("requestDate", datetime.utcnow())
        request_data["status"] = request_data.get("status", "pending")
        result = await cls.collection.insert_one(request_data)
        return str(result.inserted_id)

    @classmethod
    async def get_by_id(cls, request_id: str) -> Optional[Dict[str, Any]]:
        return await cls.collection.find_one({"_id": ObjectId(request_id)})

    @classmethod
    async def get_by_user(cls, user_id: str) -> List[Dict[str, Any]]:
        cursor = cls.collection.find({"requestedBy": ObjectId(user_id)})
        return await cursor.to_list(length=None)

    @classmethod
    async def get_by_status(cls, status: str) -> List[Dict[str, Any]]:
        cursor = cls.collection.find({"status": status})
        return await cursor.to_list(length=None)

    @classmethod
    async def get_all(cls) -> List[Dict[str, Any]]:
        cursor = cls.collection.find()
        return await cursor.to_list(length=None)

    @classmethod
    async def update_status(cls, request_id: str, status: str, response_by_id: str, notes: Optional[str] = None) -> bool:
        update_fields = {
            "status": status,
            "responseDate": datetime.utcnow(),
            "responseBy": ObjectId(response_by_id)
        }
        if notes:
            update_fields["notes"] = notes

        result = await cls.collection.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": update_fields}
        )
        return result.modified_count > 0