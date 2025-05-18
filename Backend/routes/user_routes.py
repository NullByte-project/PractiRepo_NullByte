from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.responses import JSONResponse

from config import db
from config.jwt_depends import JWTBearer, get_current_admin_user, get_current_user, has_permission
from config.jwt_manager import decode_jwt

from models.user_models import User
from controllers.user_controller import (
    change_password_controller,
    create_user_by_admin_controller,
    find_all_users_controller,
    find_user_controller,
    login_user_controller,
    register_user_controller,
    reset_password_controller,
    update_user_controller,
    delete_user_controller,
)
from schemas.user_schema import (
    PasswordChangeRequest,
    PasswordResetRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserPublic,
    UserRegistrationInput
)

# Ruta base para operaciones relacionadas con usuarios
router = APIRouter(prefix="/users", tags=["users"])

# Obtener todos los usuarios
@router.get("/", response_model=list[UserPublic])
async def find_all_users():
    return await find_all_users_controller()

# Obtener el perfil del usuario autenticado
@router.get("/mi-perfil")
async def get_profile(current_user: UserPublic = Depends(get_current_user)):
    return current_user

# Ruta protegida: requiere permiso específico para descargar documentos
@router.get("/descargar", dependencies=[Depends(has_permission("download:document"))])
async def download_document():
    return {"msg": "Acceso permitido para descargar"}

# Ruta solo accesible para administradores
@router.get("/admin-only")
async def admin_endpoint(current_admin: UserPublic = Depends(get_current_admin_user)):
    return {"msg": f"Bienvenido administrador {current_admin.name}"}

@router.post("/admin/create", response_model=UserPublic)
async def create_user_by_admin_endpoint(
    user_data: UserCreate,
    _=Depends(get_current_admin_user)  # Protección por rol admin
):
    return await create_user_by_admin_controller(user_data)

@router.get('/{id}', response_model=UserPublic)
async def find_user(id: str):
    return await find_user_controller(id)

# Actualizar un usuario existente por ID
@router.put('/{id}', response_model=UserPublic)
async def update_user(id: str, user: UserCreate):
    return await update_user_controller(id, user)

# Eliminar un usuario por ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    deleted = await delete_user_controller(id)
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# Registrar un nuevo usuario (registro extendido)
@router.post("/register", response_model=UserPublic)
async def register_user_endpoint(user_input: UserRegistrationInput):
    return await register_user_controller(user_input)

# Iniciar sesión de usuario (login)
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    token = await login_user_controller(data)
    return JSONResponse(content=token.dict(), status_code=200)

# Cambiar contraseña (requiere autenticación)
@router.post("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: UserPublic = Depends(get_current_user)
):
    return await change_password_controller(current_user.email, data)

# Solicitar restablecimiento de contraseña por email
@router.post("/reset-password")
async def reset_password(data: PasswordResetRequest):
    return await reset_password_controller(data)
