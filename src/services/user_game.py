from src.schemas.user_game import UserGameCreate
from src.repositories.repository import AbstractRepository


class UserGameService:
    def __init__(self, user_games_repo: AbstractRepository):
        self.user_games_repo: AbstractRepository = user_games_repo

    async def add_user_game(self, user_game: UserGameCreate):
        user_game_dict = user_game.model_dump()
        user_game_id = await self.user_games_repo.add_one(data=user_game_dict)
        return user_game_id

    async def get_user_games(self, **filters):
        user_games = await self.user_games_repo.get_all(**filters)
        return user_games

    async def get_user_game(self, **filters):
        user_game = await self.user_games_repo.get_one(**filters)
        return user_game

    async def delete_user_game(self, **filters):
        user_game = await self.user_games_repo.delete_one(**filters)
        return user_game