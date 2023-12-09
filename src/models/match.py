from datetime import datetime

from sqlalchemy import Column, ForeignKey, BigInteger, String, TIMESTAMP, Boolean

from src.schemas.match import MatchRead
from settings.database_connection.connection import Base


class Match(Base):
    __tablename__ = "Match"

    id = Column(BigInteger, primary_key=True)
    user1_id = Column(BigInteger, ForeignKey("User.id", ondelete="CASCADE"))
    user2_id = Column(BigInteger, ForeignKey("User.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    status = Column(Boolean, default=False)
    def to_read_model(self) -> MatchRead:
        return MatchRead(
            id=self.id,
            user1_id=self.user1_id,
            user2_id=self.user2_id,
            created_at=self.created_at
        )
