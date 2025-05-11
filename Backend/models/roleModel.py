from config.db import db
from typing import Optional
from bson import ObjectId

class RoleModel:
    collection = db["roles"]

    @classmethod
    async def create(cls, data: dict) -> str:
        result = await cls.collection.insert_one(data)
        return str(result.inserted_id)

    @classmethod
    async def get_by_id(cls, id: str) -> Optional[dict]:
        return await cls.collection.find_one({"_id": ObjectId(id)})

    @classmethod
    async def get_by_name(cls, name: str) -> Optional[dict]:
        return await cls.collection.find_one({"name": name})

    @classmethod
    async def list_all(cls):
        cursor = cls.collection.find()
        return await cursor.to_list(length=None)
