from src.schemas.game import GameCreate

from src.repositories.repository import AbstractRepository



class GameService:
    def __init__(self, games_repo: AbstractRepository):
        self.games_repo: AbstractRepository = games_repo

    async def add_game(self, game: GameCreate):
        game_dict = game.model_dump()
        game_id = await self.games_repo.add_one(data=game_dict)
        return game_id

    async def get_games(self):
        games = await self.games_repo.get_all()
        return games
    
    async def get_game(self, **filters):
        game = await self.games_repo.get_one(**filters)
        return game

    async def delete_game(self, **filters):
        game = await self.games_repo.delete_one(**filters)
        return game