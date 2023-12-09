from src.models.role import Role
from .repository import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository):
    model = Role
