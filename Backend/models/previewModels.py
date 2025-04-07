from datetime import datetime
from config.db import db
from bson import ObjectId
from typing import Dict, Any

class PreviewModel:
    collection = db["previews"]
    
    @classmethod
    def create_preview(cls, practice_id: str, fragments: Dict[str, Any]) -> str:
        preview_data = {
            "practice_id": practice_id,
            "fragments": fragments,
            "created_at": datetime.utcnow()
        }
        result = cls.collection.insert_one(preview_data)
        return str(result.inserted_id)
    
    @classmethod
    def get_preview(cls, practice_id: str) -> Dict[str, Any]:
        return cls.collection.find_one({"practice_id": practice_id})