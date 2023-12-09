from sqlalchemy import Column, BigInteger, ForeignKey, String

from src.schemas.user_game import UserGameRead
from settings.database_connection.connection import Base


class UserGame(Base):
    __tablename__ = "UserGame"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("User.id", ondelete="CASCADE"))
    game_id = Column(BigInteger, ForeignKey("Game.id", ondelete="CASCADE"))
    playtime_2weeks = Column(BigInteger, nullable=True)
    playtime_forever = Column(BigInteger, nullable=True)
    rank = Column(String)

    def to_read_model(self) -> UserGameRead:
        return UserGameRead(
            id=self.id,
            user_id=self.user_id,
            game_id=self.game_id,
            playtime_2weeks=self.playtime_2weeks,
            playtime_forever=self.playtime_forever,
            rank=self.rank
        )