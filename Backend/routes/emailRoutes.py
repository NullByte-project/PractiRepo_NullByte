from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from controllers.emailController import send_email_controller
from schemas.schemaEmail import EmailRequest, ContactFormRequest

# Router para las operaciones relacionadas con el envío de correos
router = APIRouter(prefix="/email", tags=["email"])

# Endpoint para enviar un correo electrónico genérico
@router.post("/send")
async def send_email(data: EmailRequest):
    """
    Envía un correo electrónico con los datos proporcionados.
    Parámetros:
    - to: destinatario
    - subject: asunto del correo
    - content: contenido HTML del correo
    """
    return await send_email_controller(
        to_email=data.to,
        subject=data.subject,
        html_content=data.content
    )

# Endpoint para recibir y enviar formularios de contacto al email del administrador
@router.post("/contact")
async def send_contact_form(data: ContactFormRequest):
    """
    Recibe datos del formulario de contacto y envía un correo al administrador.
    El correo incluye nombre, email, teléfono, tipo de usuario, mensaje y aceptación de términos.
    """
    # Construcción del asunto del correo
    subject = f"Contacto de {data.nombre} {data.apellidos} ({data.tipoUsuario})"

    # Construcción del contenido HTML del correo con los datos recibidos
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

    # Email del administrador que recibirá los mensajes de contacto
    admin_email = "erleycabrera062@gmail.com"

    # Intentar enviar el correo y capturar cualquier error
    try:
        return await send_email_controller(
            to_email=admin_email,
            subject=subject,
            html_content=html_content
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar mensaje de contacto: {e}"
        )

