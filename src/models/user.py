from datetime import datetime
import os
from sqlalchemy import Column, String, TIMESTAMP, Boolean, ForeignKey, BigInteger

from src.schemas.user import UserRead
from settings.database_connection.connection import Base


class User(Base):
    __tablename__ = "User"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)

    is_active: bool = Column(Boolean, default=True, nullable=False)  #
    is_superuser: bool = Column(Boolean, default=False, nullable=False)  #

    role_id = Column(BigInteger, ForeignKey('Role.id', ondelete='SET NULL'), default=1)

    steam_id = Column(String, nullable=True, unique=True, default=0)

    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            email=self.email,
            username=self.username,
            role_id=self.role_id,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            steam_id=self.steam_id
        )