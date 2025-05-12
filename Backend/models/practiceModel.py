from config.db import db
from bson import ObjectId
from typing import Dict, Any, List

class PracticeModel:
    collection = db["practices"]
    
    @classmethod
    async def create(cls, practice_data: Dict[str, Any]) -> str:
        result = await cls.collection.insert_one(practice_data)
        return str(result.inserted_id)

    @classmethod
    async def get_by_id(cls, practice_id: str) -> Dict[str, Any] | None:
        return await cls.collection.find_one({"_id": ObjectId(practice_id)})

    @classmethod
    async def get_all(cls) -> List[Dict[str, Any]]:
        cursor = cls.collection.find()
        return await cursor.to_list(length=None)  

    @classmethod
    async def get_by_type(cls, practice_type: str) -> List[Dict[str, Any]]:
        cursor = cls.collection.find({"practice_type": practice_type})
        return await cursor.to_list(length=None)

    @classmethod
    async def update(cls, practice_id: str, update_data: Dict[str, Any]) -> bool:
        result = await cls.collection.update_one(
            {"_id": ObjectId(practice_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, practice_id: str) -> bool:
        result = await cls.collection.delete_one({"_id": ObjectId(practice_id)})
        return result.deleted_count > 0