from fastapi import APIRouter, HTTPException
from controllers.previewController import generate_preview
from schemas.schemaPractice import PreviewFragment
from typing import List

router = APIRouter(prefix="/previews", tags=["previews"])

@router.get("/{practice_id}", response_model=List[PreviewFragment])
async def get_preview_fragments(practice_id: str):
    """Obtiene fragmentos de previsualización para una práctica"""
    return await generate_preview(practice_id) 