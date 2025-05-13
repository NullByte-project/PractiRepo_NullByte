from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from controllers.emailController import send_email_controller
from schemas.schemaEmail import EmailRequest

#Post a email
router = APIRouter(prefix="/email", tags=["email"])
@router.post("/send")
async def send_email(data: EmailRequest):
    return await send_email_controller(
        to_email=data.to,
        subject=data.subject,
        html_content=data.content
    )