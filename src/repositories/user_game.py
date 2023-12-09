from src.models.user_game import UserGame
from src.repositories.repository import SQLAlchemyRepository


class UserGameRepository(SQLAlchemyRepository):
    model = UserGame