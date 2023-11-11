from src.schemas.role import RoleCreate, RoleRead

from src.utils.repository import AbstractRepository


class RoleService:
    def __init__(self, role_repo: AbstractRepository):
        self.role_repo: AbstractRepository = role_repo

    async def add_role(self, token: RoleCreate):
        role_dict = token.model_dump()
        role_id = await self.role_repo.add_one(data=role_dict)
        return role_id

    async def get_role(self, token: RoleRead):
        role_dict = token.model_dump()
        role = await self.role_repo.get_one(filters=role_dict)
        return role