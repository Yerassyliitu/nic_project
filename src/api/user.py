from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import user_service
from src.schemas.user import UserCreate
from src.services.user import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)



@user_router.post("")
async def add_user(
    user: UserCreate,
    users_service: Annotated[UserService, Depends(user_service)],
):
    user_id = await users_service.add_user(user)
    return {"user_id": user_id}


@user_router.get("")
async def get_users(
    users_service: Annotated[UserService, Depends(user_service)],
):
    users = await users_service.get_users()
    return users