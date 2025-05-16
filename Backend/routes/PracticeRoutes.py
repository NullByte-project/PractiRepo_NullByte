import os
from fastapi import APIRouter, Depends, Path, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from config.jwt_depends import get_current_admin_user, get_current_user
from controllers.practiceController import (
    create_practice,
    get_practice,
    get_all_practices,
    get_practices_by_type,
    update_practice,
    delete_practice, 
    get_practices_by_filters
)
from models.documentRequestModel import DocumentRequestModel
from models.practiceModel import PracticeModel
from schemas.schemaPractice import Practice
from typing import Optional, List

from schemas.user_schema import UserPublic

router = APIRouter(prefix="/practices", tags=["practices"])

@router.post("/", response_model=Practice, status_code=201)
async def create_practice_endpoint(
    title: str = Form(...),
    year: int = Form(...),
    practice_type: str = Form(...),
    file: UploadFile = File(...),
    institution: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    municipality: Optional[str] = Form(None),
    _=Depends(get_current_admin_user)  # Protección por rol admin
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

#obtener practicas por filtro 
@router.get("/filter", response_model=List[Practice])
async def read_practices_by_filter(title: Optional[str] = None, year: Optional[int] = None, 
                                   practice_type: Optional[str] = None, institution: Optional[str] = None, author: Optional[str] = None, 
                                   municipality: Optional[str] = None):
    return await get_practices_by_filters(
        title = title,
        year=year,
        municipality=municipality,
        practice_type=practice_type,
        institution=institution,
        author=author
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
    file: Optional[UploadFile] = File(None),
    _=Depends(get_current_admin_user)  # Protección por rol admin
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
async def delete_practice_endpoint(
    practice_id: str,
    _=Depends(get_current_admin_user)  # Protección por rol admin
):
    await delete_practice(practice_id)
    return None

@router.get(
    "/{practice_id}/download",
    response_class=FileResponse,
    summary="RF12: Descarga de documento permitida solo si solicitud fue aprobada (o si es admin)",
    responses={
        403: {"description": "Acceso denegado o solicitud no aprobada"},
        404: {"description": "Práctica o archivo no encontrado"},
    }
)
async def download_practice_document_endpoint(
    practice_id: str = Path(..., description="ID de la práctica a descargar"),
    current_user: UserPublic = Depends(get_current_user)
):
    # 1. Validar que la práctica exista
    practice = await PracticeModel.get_by_id(practice_id)
    if not practice:
        raise HTTPException(status_code=404, detail="Práctica no encontrada")

    # 2. Verificar que exista el archivo
    document_path = practice.get("document_path")
    if not document_path or not os.path.exists(document_path):
        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado en el servidor o ruta inválida."
        )

    # 3. Verificar si el usuario es administrador
    try:
        admin_user = await get_current_admin_user(current_user)
        is_admin = True
    except HTTPException as e:
        if e.status_code == 403:
            is_admin = False
        else:
            raise e

    # 4. Si no es admin, verificar solicitud aprobada
    if not is_admin:
        approved = await DocumentRequestModel.find_approved_request(
            practice_id=practice_id,
            user_id=current_user.id
        )
        if not approved:
            raise HTTPException(
                status_code=403,
                detail="Acceso denegado: no tienes una solicitud aprobada para este documento."
            )

    # 5. Enviar archivo
    return FileResponse(
        path=document_path,
        filename=os.path.basename(document_path),
        media_type='application/octet-stream'
    )