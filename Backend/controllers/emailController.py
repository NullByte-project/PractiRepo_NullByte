import base64
import os
from typing import Optional
import sib_api_v3_sdk
from fastapi import APIRouter, HTTPException
from sib_api_v3_sdk.rest import ApiException
from pydantic import EmailStr

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")


async def send_email_controller(to_email: EmailStr, subject: str, html_content: str):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "erleycabrera99@gmail.com", "name": "PractiRepo"},
        subject=subject,
        html_content=html_content
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return {"status": "ok", "message_id": api_response.message_id}
    except ApiException as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar correo: {e}")
    
    
async def send_email_controller_for_documentsRequest(
    to_email: EmailStr,
    subject: str,
    html_content: str,
    attachment_path: Optional[str] = None, # Ruta al archivo a adjuntar
    attachment_name: Optional[str] = None  # Nombre que tendrá el archivo en el correo
):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    attachments = []
    if attachment_path and os.path.exists(attachment_path):
        try:
            with open(attachment_path, "rb") as f:
                file_content = f.read()
            
            encoded_content = base64.b606(file_content).decode() # Brevo espera base64
            
            attachments.append(
                sib_api_v3_sdk.SendSmtpEmailAttachment(
                    content=encoded_content,
                    name=attachment_name or os.path.basename(attachment_path)
                )
            )
        except Exception as e:
            print(f"Error al preparar el adjunto '{attachment_path}': {e}")
            # Decidir si fallar el envío de correo o enviarlo sin adjunto
            # Por ahora, se enviará sin adjunto si este paso falla.

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "erleycabrera99@gmail.com", "name": "PractiRepo"}, # Considera hacerlo configurable
        subject=subject,
        html_content=html_content,
        attachment=attachments if attachments else None # Añadir adjuntos
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email enviado, Message ID: {api_response.message_id}")
        return {"status": "ok", "message_id": api_response.message_id}
    except ApiException as e:
        print(f"Error de API de Brevo al enviar correo a {to_email}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al enviar correo: {e.body if hasattr(e, 'body') else e}")
    except Exception as e:
        print(f"Error general al enviar correo a {to_email}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al enviar correo: {str(e)}")
