from src.models.match import Match
from .repository import SQLAlchemyRepository


class MatchRepository(SQLAlchemyRepository):
    model = Match