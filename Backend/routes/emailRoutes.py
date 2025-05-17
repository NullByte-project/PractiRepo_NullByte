from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from controllers.emailController import send_email_controller
from schemas.schemaEmail import EmailRequest
from schemas.schemaEmail import ContactFormRequest

#Post a email
router = APIRouter(prefix="/email", tags=["email"])
@router.post("/send")
async def send_email(data: EmailRequest):
    return await send_email_controller(
        to_email=data.to,
        subject=data.subject,
        html_content=data.content
    )

@router.post("/contact")
async def send_contact_form(data: ContactFormRequest):
    # Construir asunto y HTML
    subject = f"Contacto de {data.nombre} {data.apellidos} ({data.tipoUsuario})"
    html_content = f"""
    <html>
    <body>
        <h2>Nuevo mensaje de contacto</h2>
        <p><strong>Nombre completo:</strong> {data.nombre} {data.apellidos}</p>
        <p><strong>Email:</strong> {data.email}</p>
        <p><strong>Teléfono:</strong> {data.telefono or 'No proporcionado'}</p>
        <p><strong>Tipo de usuario:</strong> {data.tipoUsuario}</p>
        <p><strong>Mensaje:</strong></p>
        <p>{data.mensaje or 'No hay mensaje'}</p>
        <p><strong>Aceptó términos:</strong> {"Sí" if data.terminos else "No"}</p>
    </body>
    </html>
    """
    admin_email = "erleycabrera062@gmail.com"

    try:
        return await send_email_controller(
            to_email=admin_email,
            subject=subject,
            html_content=html_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar mensaje de contacto: {e}")
