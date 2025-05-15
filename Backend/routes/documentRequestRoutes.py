# routes/document_request_routes.py
from fastapi import APIRouter, Depends, Path, Body, Query, status as http_status # Importar status
from typing import List, Optional

from schemas.schemaDocumentRequest import (
    DocumentRequestPublic,
    DocumentRequestUpdateAdmin,
    DocumentRequestStatus,
    # DocumentRequestCreate # Ya no se usa como body si practice_id es path param
)
from schemas.user_schema import UserPublic
from controllers.documentRequestController import (
    create_document_request_controller,
    get_my_document_requests_controller,
    get_all_document_requests_admin_controller,
    manage_document_request_admin_controller
)
# Asegúrate que la ruta a tus dependencias de JWT sea correcta
from config.jwt_depends import get_current_user, get_current_admin_user, has_permission

router = APIRouter(prefix="/document-requests", tags=["Document Download Requests"])

@router.post(
    "/request/{practice_id}",
    response_model=DocumentRequestPublic,
    summary="RF10: Usuario solicita descargar un documento",
    status_code=http_status.HTTP_201_CREATED # Código correcto para creación exitosa
)
async def request_document_download_endpoint(
    practice_id: str = Path(..., description="ID de la práctica a solicitar"),
    current_user: UserPublic = Depends(get_current_user),
    # Asegúrate que el permiso "request_download" esté asignado a los roles de usuario correspondientes
    # y que se incluya en el token JWT durante el login.
    # _=Depends(has_permission("request_download")) # Descomentar si ya tienes la gestión de permisos en JWT lista
):
    # La dependencia has_permission ya lanzaría HTTPException si no tiene el permiso.
    return await create_document_request_controller(practice_id=practice_id, current_user=current_user)


@router.get(
    "/my-requests",
    response_model=List[DocumentRequestPublic],
    summary="Usuario obtiene sus propias solicitudes de descarga"
)
async def get_my_download_requests_endpoint(
    current_user: UserPublic = Depends(get_current_user)
):
    return await get_my_document_requests_controller(current_user=current_user)


# --- Rutas para Administradores ---
@router.get(
    "/admin/all",
    response_model=List[DocumentRequestPublic],
    summary="RF11: Administrador obtiene todas las solicitudes de descarga (puede filtrar por estado)"
)
async def get_all_download_requests_for_admin_endpoint(
    status: Optional[DocumentRequestStatus] = Query(None, description="Filtrar por estado de la solicitud"),
    # current_admin: UserPublic = Depends(get_current_admin_user) # La dependencia ya valida
    _=Depends(get_current_admin_user) # Solo para proteger la ruta
):
    return await get_all_document_requests_admin_controller(status=status)


@router.put(
    "/admin/manage/{request_id}",
    response_model=DocumentRequestPublic,
    summary="RF11 y RF12: Administrador aprueba o rechaza una solicitud de descarga"
)
async def manage_download_request_by_admin_endpoint(
    request_id: str = Path(..., description="ID de la solicitud a gestionar"),
    update_data: DocumentRequestUpdateAdmin = Body(...),
    current_admin: UserPublic = Depends(get_current_admin_user) # Para obtener el ID del admin
):
    return await manage_document_request_admin_controller(
        request_id=request_id,
        update_data=update_data,
        current_admin=current_admin
    )