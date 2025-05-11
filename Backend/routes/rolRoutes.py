from fastapi import APIRouter
from schemas.role_schema import RoleCreate, RolePublic
from controllers.rolController import create_role_controller, list_roles_controller

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RolePublic)
async def create_role(data: RoleCreate):
    return await create_role_controller(data)

@router.get("/", response_model=list[RolePublic])
async def get_all_roles():
    return await list_roles_controller()