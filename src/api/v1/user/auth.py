from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import DecodeError

from src.api.dependencies import user_service
from src.utils.auth_handler import get_current_user, bcrypt_context, create_access_token, \
    create_refresh_token, decode_token
from src.schemas.user import UserCreate, RefreshInput
from src.services.user import UserService


auth_router = APIRouter(prefix="/v1/auth", tags=["auth"])


@auth_router.post(
    "/signup/",
    status_code=201,
    summary="Регистрация пользователя.",
)
async def add_user(
        user: UserCreate,
        users_service: Annotated[UserService, Depends(user_service)],
):
    user_id = await users_service.add_user(user)
    return {"user_id": user_id}


@auth_router.post(
    "/login/",
    status_code=200,
    summary="Вход в систему.",
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        users_service: Annotated[UserService, Depends(user_service)],
):
    user = await users_service.get_user(username=form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Неправильный пароль")
    data = {'email': user.email, 'id': user.id, 'username': user.username, 'user_role': user.role_id,
            'steam_id': user.steam_id}
    token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {'access_token': token, 'token_type': 'bearer', 'refresh_token': refresh_token}


@auth_router.post(
    "/refresh/",
    status_code=200,
    summary="Обновление access token.",
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




@auth_router.post(
    "/current-user/",
    status_code=200,
    summary="Возвращает пользователя.",
    description="Возвращает пользователя.",
)
async def get_user(
        user: Annotated[dict, Depends(get_current_user)],
):
    return {'user': user}

