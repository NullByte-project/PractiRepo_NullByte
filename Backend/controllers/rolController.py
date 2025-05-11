from models.roleModel import RoleModel
from schemas.role_schema import RoleCreate, RolePublic

async def create_role_controller(data: RoleCreate) -> RolePublic:
    role_dict = data.dict()
    inserted_id = await RoleModel.create(role_dict)
    role_dict["_id"] = inserted_id
    return RolePublic(**role_dict)

async def get_role_by_name_controller(name: str) -> RolePublic:
    db_role = await RoleModel.get_by_name(name)
    if db_role:
        db_role["id"] = str(db_role["_id"])
        return RolePublic(**db_role)
    return None

async def list_roles_controller() -> list[RolePublic]:
    roles = await RoleModel.list_all()
    return [RolePublic(**{**role, "_id": str(role["_id"])}) for role in roles]
