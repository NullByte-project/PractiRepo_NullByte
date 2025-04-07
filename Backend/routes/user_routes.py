from fastapi import APIRouter, Response, status
from models.user_models import User
from controllers.user_controller import (
    find_all_users_controller,
    create_user_controller,
    find_user_controller,
    update_user_controller,
    delete_user_controller,
)

user = APIRouter(tags=["users"])

@user.get('/users', response_model=list[User])
def find_all_users():
    return find_all_users_controller()

@user.post('/users', response_model=User)
def create_user(user: User):
    return create_user_controller(user)

@user.get('/users/{id}', response_model=User)
def find_user(id: str):
    return find_user_controller(id)

@user.put('/users/{id}', response_model=User)
def update_user(id: str, user: User):
    return update_user_controller(id, user)

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    deleted = delete_user_controller(id)
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)