from fastapi import HTTPException
from typing import List, Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import user_game_service
from src.schemas.user_game import UserGameRead, UserGameCreate
from src.services.user_game import UserGameService


user_game_router = APIRouter(prefix="/v1/user_game", tags=["user_game"])

@user_game_router.post(
    "/",
    status_code=201,
    summary="Добавляет игру к базе игр пользователя",
    description="Добавляет игру к базе игр пользователя",
)
async def add_user_game(
        user_game: UserGameCreate,
        user_games_service: Annotated[UserGameService, Depends(user_game_service)],
):
    user_game = await user_games_service.add_user_game(user_game=user_game)
    if user_game:
        return user_game
    else:
        raise HTTPException(status_code=404, detail="User game not found")



@user_game_router.get(
    "/all/",
    status_code=200,
    response_model=List[UserGameRead],
    summary="Возвращает все игры пользователя",
)
async def get_user_games(
        user_games_service: Annotated[UserGameService, Depends(user_game_service)]
):
    user_games = await user_games_service.get_user_games()
    if user_games:
        return user_games
    else:
        raise HTTPException(status_code=404, detail="User games not found")


@user_game_router.get(
    "/{id}",
    response_model=UserGameRead,
    status_code=200,
    summary="Возвращает игру пользователя по id",
)
async def get_user_game(
        user_games_service: Annotated[UserGameService, Depends(user_game_service)],
        id: int
):
    user_game = await user_games_service.get_user_game(id=id)
    if user_game:
        return user_game
    else:
        raise HTTPException(status_code=404, detail="User game not found")


@user_game_router.delete(
    "/{id}",
    response_model=UserGameRead,
    status_code=200,
    summary="Удаляет игру пользователя по id",
)
async def delete_user_game(
        user_games_service: Annotated[UserGameService, Depends(user_game_service)],
        id: int,
):
    user_game = await user_games_service.delete_user_game(id=id)
    if user_game:
        return user_game
    else:
        raise HTTPException(status_code=404, detail="User game not found")
