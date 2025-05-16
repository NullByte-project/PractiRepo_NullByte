from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.responses import JSONResponse
from config import db
from config.jwt_depends import JWTBearer, get_current_admin_user, get_current_user, has_permission
from config.jwt_manager import decode_jwt
from models.user_models import User
from controllers.user_controller import (
    change_password_controller,
    find_all_users_controller,
    find_user_controller,
    login_user_controller,
    register_user_controller,
    reset_password_controller,
    update_user_controller,
    delete_user_controller,
)
from schemas.user_schema import PasswordChangeRequest, PasswordResetRequest, TokenResponse, UserCreate, UserLogin, UserPublic, UserRegistrationInput

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserPublic])
async def find_all_users():
    return await find_all_users_controller()

@router.get("/mi-perfil")
async def get_profile(current_user: UserPublic = Depends(get_current_user)):
    return current_user

@router.get("/descargar", dependencies=[Depends(has_permission("download:document"))])
async def download_document():
    return {"msg": "Acceso permitido para descargar"}

@router.get("/admin-only")
async def admin_endpoint(current_admin: UserPublic = Depends(get_current_admin_user)):
    return {"msg": f"Bienvenido administrador {current_admin.name}"}

@router.get('/{id}', response_model=UserPublic)
async def find_user(id: str):
    return await find_user_controller(id)

@router.put('/{id}', response_model=UserPublic)
async def update_user(id: str, user: UserCreate):
    return await update_user_controller(id, user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    deleted = await delete_user_controller(id)
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

#Logica de login
# @router.post("/register", response_model=UserPublic)
# async def register_user(data: UserCreate):
#     return await register_user_controller(data)

@router.post("/register", response_model=UserPublic)
async def register_user_endpoint(user_input: UserRegistrationInput):
    return await register_user_controller(user_input)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    token = await login_user_controller(data)
    return JSONResponse(content=token.dict(), status_code=200)

@router.post("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: UserPublic = Depends(get_current_user)
):
    return await change_password_controller(current_user.email, data)

@router.post("/reset-password")
async def reset_password(data: PasswordResetRequest):
    return await reset_password_controller(data)