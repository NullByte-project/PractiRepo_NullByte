import os
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
