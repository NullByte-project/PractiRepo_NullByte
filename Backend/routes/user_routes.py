from fastapi import APIRouter, Response, status
from models.user_models import User
from controllers.user_controller import (
    find_all_users_controller,
    create_user_controller,
    find_user_controller,
    update_user_controller,
    delete_user_controller,
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[User])
async def find_all_users():
    return await find_all_users_controller()

@router.get('/', response_model=list[User])
def find_all_users():
    return find_all_users_controller()

@router.get('/', response_model=list[User])
async def find_all_users():
    return await find_all_users_controller()

@router.post('/', response_model=User)
async def create_user(user: User):
    return await create_user_controller(user)

@router.get('/{id}', response_model=User)
async def find_user(id: str):
    return await find_user_controller(id)

@router.put('/{id}', response_model=User)
async def update_user(id: str, user: User):
    return await update_user_controller(id, user)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    deleted = await delete_user_controller(id)
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)