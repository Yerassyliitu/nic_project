from src.schemas.user import UserCreate
from src.schemas.auth import RefreshInput

from src.utils.repository import AbstractRepository
from src.utils.auth_handler import bcrypt_context


class UserService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo

    async def add_user(self, user: UserCreate):
        user_dict = user.model_dump()
        hashed_password = bcrypt_context.hash(user_dict["password"])
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password

        user_id = await self.users_repo.add_one(data=user_dict)
        return user_id

    async def get_users(self):
        users = await self.users_repo.get_all()
        return users

    async def get_user(self, filters):
        user = await self.users_repo.get_one(filters=filters)
        return user

