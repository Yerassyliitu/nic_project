from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import user_service
from src.schemas.user import UserRead, UserEdit
from src.services.user import UserService



user_router = APIRouter(prefix="/v1/user", tags=["user"])


@user_router.get(
    "/",
    response_model=List[UserRead],
    status_code=200,
    summary="Возвращает всех пользователей",
)
async def get_users(
        users_service: Annotated[UserService, Depends(user_service)],
):
    users = await users_service.get_users()
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="Users not found")


@user_router.get(
    "/{id}",
    response_model=UserRead,
    status_code=200,
    summary="Возвращает пользователя по id",
)
async def get_user(
        users_service: Annotated[UserService, Depends(user_service)],
        id: int
):
    user = await users_service.get_user(id=id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.put(
    "/{id}",
    response_model=UserRead,
    status_code=200,
    summary="Обновляет пользователя по id",
)
async def edit_user(
        users_service: Annotated[UserService, Depends(user_service)],
        id: int,
        user: UserEdit,
):
    user = await users_service.edit_user(id=id, user=user)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.delete(
    "/{id}",
    response_model=UserRead,
    status_code=200,
    summary="Удаляет пользователя по id",
)
async def delete_user(
        users_service: Annotated[UserService, Depends(user_service)],
        id: int
):
    user = await users_service.delete_user(id=id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

