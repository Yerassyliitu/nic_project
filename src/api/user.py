from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import DecodeError

from src.schemas.auth import RefreshInput
from src.utils.auth_handler import bcrypt_context, create_refresh_token, create_access_token, decode_token, \
    get_current_user
from .dependencies import user_service, token_service
from src.schemas.user import UserCreate
from src.services.user import UserService
from src.services.auth import TokenService


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post("/signup")
async def add_user(
        user: UserCreate,
        users_service: Annotated[UserService, Depends(user_service)],
):
    user_id = await users_service.add_user(user)
    return {"user_id": user_id}


@user_router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        users_service: Annotated[UserService, Depends(user_service)],
):
    filters = {"username": form_data.username}
    user = await users_service.get_user(filters=filters)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Неправильный пароль")
    data = {'email': user.email, 'id': user.id, 'username': user.username, 'user_role': user.role_id}
    token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {'access_token': token, 'token_type': 'bearer', 'refresh_token': refresh_token}


@user_router.post(
    "/refresh/"
)
async def refresh_token_router(
        request: Annotated[RefreshInput, Depends()],
):
    try:
        refresh_token = request.refresh_token
        payload = decode_token(refresh_token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        current_time = datetime.utcnow()
        token_expiration = datetime.fromtimestamp(payload["exp"])
        if current_time > token_expiration:
            raise HTTPException(status_code=401, detail="Refresh token has expired")

        email: str = payload.get('sub')
        username: str = payload.get('username')
        id: int = payload.get('id')
        user_role: int = payload.get('user_role')

        # Создайте новый access_token с собственным payload
        new_access_token_payload = {'email': email, 'id': id, 'username': username, 'user_role': user_role}

        access_token = create_access_token(data=new_access_token_payload)

        return {"access_token": access_token, "token_type": "bearer"}
    except DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")


@user_router.get("/")
async def get_users(
        users_service: Annotated[UserService, Depends(user_service)],
):
    users = await users_service.get_users()
    return users




@user_router.post(
    "/logout/"
)
async def logout(
        tokens_service: Annotated[TokenService, Depends(token_service)],
        token: RefreshInput
):
    if_token = await tokens_service.get_revoked_token(token)
    if if_token:
        raise HTTPException(status_code=400, detail="Token has already been revoked")
    await tokens_service.add_revoked_token(token)
    return {"message": "You have been logged out"}



@user_router.post(
    "/current-user/",
    status_code=200,
    summary="Возвращает пользователя.",
    description="Возвращает пользователя.",
    tags=["auth"]
)
async def get_user(
        user: Annotated[dict, Depends(get_current_user)],
):
    return {'user': user}
