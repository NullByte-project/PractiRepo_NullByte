from fastapi import HTTPException, Depends
from typing import List, Optional
import os
from datetime import datetime
from bson import ObjectId

from models.documentRequestModel import DocumentRequestModel
from models.practiceModel import PracticeModel
from schemas.schemaDocumentRequest import (
    DocumentRequestPublic,
    DocumentRequestUpdateAdmin,
    DocumentRequestStatus
)
from schemas.user_schema import UserPublic
from controllers.emailController import send_email_controller, send_email_controller_for_documentsRequest
from config.jwt_depends import get_current_user, get_current_admin_user

ADMIN_EMAIL_RECIPIENT = os.getenv("ADMIN_EMAIL_RECIPIENT", "admin_default@example.com")


def sanitize_ids(data: dict) -> dict:
    for field in ["_id", "practice_id", "requested_by_id", "response_by_id"]:
        if field in data and isinstance(data[field], ObjectId):
            data[field] = str(data[field])
    return data


# -------------------------------
# RF10: Usuario solicita descarga
# -------------------------------
async def create_document_request_controller(
    practice_id: str,
    current_user: UserPublic = Depends(get_current_user)
) -> DocumentRequestPublic:
    practice = await PracticeModel.get_by_id(practice_id)
    if not practice:
        raise HTTPException(status_code=404, detail=f"Practice with id {practice_id} not found")

    if await DocumentRequestModel.check_existing_request(practice_id, current_user.id):
        raise HTTPException(status_code=400, detail="You already have a pending or approved request for this document.")

    try:
        new_request_id = await DocumentRequestModel.create(practice_id, current_user.id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    request_data_dict = await DocumentRequestModel.get_by_id_enriched(new_request_id)
    if not request_data_dict:
        raise HTTPException(status_code=500, detail="Failed to create or retrieve document request after creation.")

    # Notificación por correo
    try:
        subject = f"Nueva Solicitud de Descarga de Documento: {practice.get('title', 'N/A')}"
        html_content = f"""
        <p>Hola Administrador,</p>
        <p>El usuario <strong>{current_user.name}</strong> (Email: {current_user.email}) ha solicitado la descarga del documento:</p>
        <ul>
            <li><strong>Título:</strong> {practice.get('title', 'N/A')}</li>
            <li><strong>ID de Práctica:</strong> {practice_id}</li>
            <li><strong>ID de Solicitud:</strong> {new_request_id}</li>
        </ul>
        """
        await send_email_controller_for_documentsRequest(
            to_email=ADMIN_EMAIL_RECIPIENT,
            subject=subject,
            html_content=html_content
        )
    except Exception as e:
        print(f"[Correo Admin] Falló notificación: {e}")

    return DocumentRequestPublic(**sanitize_ids(request_data_dict))


# --------------------------------------------------
# RF10.1: Ver historial de solicitudes del usuario
# --------------------------------------------------
async def get_my_document_requests_controller(
    current_user: UserPublic = Depends(get_current_user)
) -> List[DocumentRequestPublic]:
    requests_dicts = await DocumentRequestModel.get_by_user_enriched(current_user.id)
    return [DocumentRequestPublic(**sanitize_ids(r_dict)) for r_dict in requests_dicts]


# ------------------------------------------
# RF11: Admin lista todas las solicitudes
# ------------------------------------------
async def get_all_document_requests_admin_controller(
    status: Optional[DocumentRequestStatus] = None,
    _=Depends(get_current_admin_user)  # Protección por rol admin
) -> List[DocumentRequestPublic]:
    results_dicts = await DocumentRequestModel.get_all_enriched(status_filter=status)
    return [DocumentRequestPublic(**sanitize_ids(r_dict)) for r_dict in results_dicts]


# -----------------------------------------
# RF11 + RF12: Admin gestiona la solicitud
# -----------------------------------------
async def manage_document_request_admin_controller(
    request_id: str,
    update_data: DocumentRequestUpdateAdmin,
    current_admin: UserPublic = Depends(get_current_admin_user)
) -> DocumentRequestPublic:
    request_info_dict = await DocumentRequestModel.get_by_id_enriched(request_id)
    if not request_info_dict:
        raise HTTPException(status_code=404, detail=f"Document request with id {request_id} not found")
    
    
    if request_info_dict.get("status") != DocumentRequestStatus.PENDING.value:
        raise HTTPException(status_code=400, detail=f"Only PENDING requests can be managed. Current status: {request_info_dict.get('status')}")

    if update_data.status not in [DocumentRequestStatus.APPROVED, DocumentRequestStatus.REJECTED]:
        raise HTTPException(status_code=400, detail="Admin can only set status to APPROVED or REJECTED.")

    success = await DocumentRequestModel.update_status_by_admin(
        request_id=request_id,
        new_status=update_data.status,
        admin_id=current_admin.id,
        admin_notes=update_data.admin_notes
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to update document request status in the database.")

    updated_request_dict = await DocumentRequestModel.get_by_id_enriched(request_id)
    if not updated_request_dict:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated request details.")

    # --- Correo al usuario ---
    try:
        user_email = updated_request_dict.get("requester_email")
        user_name = updated_request_dict.get("requester_name", "Usuario")
        practice_title = updated_request_dict.get("practice_title", "un documento")
        practice_id_for_file = str(updated_request_dict.get("practice_id"))

        if user_email and "@" in user_email:
            status_string_email = "APROBADA" if update_data.status == DocumentRequestStatus.APPROVED else "RECHAZADA"
            email_subject = f"Actualización de tu Solicitud de Descarga: '{practice_title}' ha sido {status_string_email}"

            email_html_content = f"<p>Hola {user_name},</p><p>Tu solicitud para <strong>{practice_title}</strong> ha sido <strong>{status_string_email}</strong>.</p>"

            attachment_file_path = None
            attachment_file_name = None

            if update_data.status == DocumentRequestStatus.APPROVED:
                practice_doc = await PracticeModel.get_by_id(practice_id_for_file)
                if practice_doc and practice_doc.get("document_path"):
                    attachment_file_path = practice_doc["document_path"]
                    if os.path.exists(attachment_file_path):
                        attachment_file_name = os.path.basename(attachment_file_path)
                        email_html_content += "<p>El documento solicitado está adjunto a este correo.</p>"
                    else:
                        email_html_content += "<p>Error al adjuntar el documento. Contacta al administrador.</p>"
                        attachment_file_path = None
                else:
                    email_html_content += "<p>Documento no encontrado. Contacta al administrador.</p>"

            elif update_data.status == DocumentRequestStatus.REJECTED:
                email_html_content += "<p>Lamentamos informarte que no podrás descargar este documento.</p>"

            if update_data.admin_notes:
                email_html_content += f"<p><strong>Notas del administrador:</strong> {update_data.admin_notes}</p>"

            await send_email_controller_for_documentsRequest(
                to_email=user_email,
                subject=email_subject,
                html_content=email_html_content,
                attachment_path=attachment_file_path,
                attachment_name=attachment_file_name
            )
    except Exception as e:
        print(f"[Correo Usuario] Error al notificar solicitud {request_id}: {e}")

    return DocumentRequestPublic(**sanitize_ids(updated_request_dict))
