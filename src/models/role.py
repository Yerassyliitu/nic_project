from sqlalchemy import Column, String, JSON, BigInteger

from settings.database_connection.connection import Base


class Role(Base):
    __tablename__ = "Role"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)  # name of role(etc. user, moderator, manager)
    permissions = Column(JSON, default={})  # permissions of that user(etc. edit, view)




