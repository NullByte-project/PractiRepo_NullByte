from pydantic import BaseModel, EmailStr

class ContactFormRequest(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str = ""
    mensaje: str = ""
    tipoUsuario: str
    terminos: bool


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    content: str