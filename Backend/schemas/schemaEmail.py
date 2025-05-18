from pydantic import BaseModel, EmailStr

# Esquema para representar la información enviada desde un formulario de contacto
class ContactFormRequest(BaseModel):
    nombre: str  # Nombre del remitente
    apellidos: str  # Apellidos del remitente
    email: EmailStr  # Correo electrónico válido
    telefono: str = ""  # Número de teléfono (opcional, por defecto vacío)
    mensaje: str = ""  # Mensaje del usuario (opcional, por defecto vacío)
    tipoUsuario: str  # Tipo de usuario (por ejemplo: estudiante, docente, etc.)
    terminos: bool  # Confirmación de aceptación de términos y condiciones

# Esquema para representar una solicitud de envío de correo electrónico
class EmailRequest(BaseModel):
    to: EmailStr  # Correo electrónico del destinatario
    subject: str  # Asunto del correo
    content: str  # Contenido del mensaje
