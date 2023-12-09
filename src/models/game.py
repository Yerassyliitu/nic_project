from sqlalchemy import Column, String, BigInteger
from schemas.game import GameRead
from settings.database_connection.connection import Base


class Game(Base):
    __tablename__ = "Game"
    id = Column(BigInteger, primary_key=True)
    app_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)
    img_icon_url = Column(String, nullable=False)

    def to_read_model(self) -> GameRead:
        return GameRead(
            id=self.id,
            app_id=self.app_id,
            name=self.name,
            img_icon_url=self.img_icon_url
        )

