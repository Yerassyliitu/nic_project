from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger

from settings.database_connection.connection import Base


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(BigInteger, primary_key=True, unique=True)
    jti = Column(String, nullable=False)
    revoked_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)