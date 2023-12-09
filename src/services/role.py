from src.schemas.role import RoleCreate, RoleRead

from src.repositories.repository import AbstractRepository


class RoleService:
    def __init__(self, role_repo: AbstractRepository):
        self.role_repo: AbstractRepository = role_repo

    async def add_role(self, role: RoleCreate):
        role_dict = role.model_dump()
        role_id = await self.role_repo.add_one(data=role_dict)
        return role_id

    async def get_role(self, **filters):
        role = await self.role_repo.get_one(**filters)
        return role

    async def get_roles(self):
        roles = await self.role_repo.get_all()
        return roles

    async def edit_role(self, role: RoleCreate, **filters):
        role_dict = role.model_dump()
        role = await self.role_repo.edit_one(**filters, data=role_dict)
        return role

    async def delete_role(self, **filters):
        return await self.role_repo.delete_one(**filters)
