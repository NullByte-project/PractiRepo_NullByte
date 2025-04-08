from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from controllers.practiceController import (
    create_practice,
    get_practice,
    get_all_practices,
    get_practices_by_type,
    update_practice,
    delete_practice
)
from schemas.schemaPractice import Practice
from typing import Optional, List

router = APIRouter(prefix="/practices", tags=["practices"])

@router.post("/", response_model=Practice, status_code=201)
async def create_practice_endpoint(
    title: str = Form(...),
    year: int = Form(...),
    practice_type: str = Form(...),
    file: UploadFile = File(...),
    institution: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    municipality: Optional[str] = Form(None)
):
    return await create_practice(
        title=title,
        year=year,
        practice_type=practice_type,
        file=file,
        institution=institution,
        author=author,
        municipality=municipality
    )

@router.get("/{practice_id}", response_model=Practice)
async def read_practice(practice_id: str):
    return await get_practice(practice_id)

@router.get("/", response_model=List[Practice])
async def read_all_practices():
    return await get_all_practices()

@router.get("/type/{practice_type}", response_model=List[Practice])
async def read_practices_by_type(practice_type: str):
    return await get_practices_by_type(practice_type)

@router.put("/{practice_id}", response_model=Practice)
async def update_practice_endpoint(
    practice_id: str,
    title: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    practice_type: Optional[str] = Form(None),
    institution: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    municipality: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    return await update_practice(
        practice_id=practice_id,
        title=title,
        year=year,
        practice_type=practice_type,
        institution=institution,
        author=author,
        municipality=municipality,
        file=file
    )

@router.delete("/{practice_id}", status_code=204)
async def delete_practice_endpoint(practice_id: str):
    await delete_practice(practice_id)
    return None