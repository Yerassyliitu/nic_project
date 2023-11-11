from src.models.auth import RevokedToken
from src.utils.repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = RevokedToken
