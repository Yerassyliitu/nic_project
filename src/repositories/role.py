from src.models.role import Role
from src.utils.repository import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository):
    model = Role
