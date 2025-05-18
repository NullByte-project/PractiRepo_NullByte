# routes/document_request_routes.py
from fastapi import APIRouter, Depends, Path, Body, Query, status as http_status
from typing import List, Optional

from schemas.schemaDocumentRequest import (
    DocumentRequestPublic,
    DocumentRequestUpdateAdmin,
    DocumentRequestStatus,
)
from schemas.user_schema import UserPublic
from controllers.documentRequestController import (
    create_document_request_controller,
    get_my_document_requests_controller,
    get_all_document_requests_admin_controller,
    manage_document_request_admin_controller
)
from config.jwt_depends import get_current_user, get_current_admin_user, has_permission

# Definición del router para las solicitudes de descarga de documentos
router = APIRouter(prefix="/document-requests", tags=["Document Download Requests"])

@router.post(
    "/request/{practice_id}",
    response_model=DocumentRequestPublic,
    summary="RF10: Usuario solicita descargar un documento",
    status_code=http_status.HTTP_201_CREATED  # Código HTTP 201 para creación exitosa
)
async def request_document_download_endpoint(
    practice_id: str = Path(..., description="ID de la práctica a solicitar"),
    current_user: UserPublic = Depends(get_current_user),
    # _=Depends(has_permission("request_download")) # Descomentar si se usa control de permisos por JWT
):
    """
    Endpoint para que un usuario solicite la descarga de un documento.
    Recibe el ID de la práctica y el usuario autenticado.
    Retorna la solicitud creada.
    """
    # La dependencia has_permission lanzaría HTTPException si no tiene permiso
    return await create_document_request_controller(practice_id=practice_id, current_user=current_user)

@router.get(
    "/my-requests",
    response_model=List[DocumentRequestPublic],
    summary="Usuario obtiene sus propias solicitudes de descarga"
)
async def get_my_download_requests_endpoint(
    current_user: UserPublic = Depends(get_current_user)
):
    """
    Endpoint para que un usuario consulte sus solicitudes de descarga.
    Retorna una lista de solicitudes realizadas por el usuario actual.
    """
    return await get_my_document_requests_controller(current_user=current_user)

# --- Rutas exclusivas para administradores ---

@router.get(
    "/admin/all",
    response_model=List[DocumentRequestPublic],
    summary="RF11: Administrador obtiene todas las solicitudes de descarga (filtrables por estado)"
)
async def get_all_download_requests_for_admin_endpoint(
    status: Optional[DocumentRequestStatus] = Query(None, description="Filtrar solicitudes por estado"),
    _=Depends(get_current_admin_user)  # Protección para solo administradores
):
    """
    Endpoint para que un administrador obtenga todas las solicitudes de descarga.
    Permite filtrar por estado (pendiente, aprobado, rechazado, descargado).
    """
    return await get_all_document_requests_admin_controller(status=status)

@router.put(
    "/admin/manage/{request_id}",
    response_model=DocumentRequestPublic,
    summary="RF11 y RF12: Administrador aprueba o rechaza una solicitud de descarga"
)
async def manage_download_request_by_admin_endpoint(
    request_id: str = Path(..., description="ID de la solicitud a gestionar"),
    update_data: DocumentRequestUpdateAdmin = Body(...),
    current_admin: UserPublic = Depends(get_current_admin_user)
):
    """
    Endpoint para que un administrador actualice el estado de una solicitud de descarga.
    Recibe el ID de la solicitud, los datos de actualización y el usuario administrador.
    Retorna la solicitud actualizada.
    """
    return await manage_document_request_admin_controller(
        request_id=request_id,
        update_data=update_data,
        current_admin=current_admin
    )
