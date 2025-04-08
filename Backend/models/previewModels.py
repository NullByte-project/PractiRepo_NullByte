from config.db import db
from datetime import datetime
from bson import ObjectId
from typing import Dict, Any

class PreviewModel:
    collection = db["previews"]

    @classmethod
    async def create_preview(cls, practice_id: str, fragments: list) -> str:
        preview_data = {
            "practice_id": practice_id,
            "fragments": fragments,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await cls.collection.insert_one(preview_data)
        return str(result.inserted_id)

    @classmethod
    async def get_preview(cls, practice_id: str) -> Dict[str, Any] | None:
        return await cls.collection.find_one({"practice_id": practice_id})

    @classmethod
    async def update_preview(cls, practice_id: str, fragments: list) -> bool:
        result = await cls.collection.update_one(
            {"practice_id": practice_id},
            {
                "$set": {
                    "fragments": fragments,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        return result.modified_count > 0