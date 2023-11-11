from src.schemas.auth import RefreshInput

from src.utils.repository import AbstractRepository


class TokenService:
    def __init__(self, token_repo: AbstractRepository):
        self.token_repo: AbstractRepository = token_repo

    async def add_revoked_token(self, token: RefreshInput):
        token_dict = token.model_dump()
        token_id = await self.token_repo.add_one(data=token_dict)
        return token_id

    async def get_revoked_token(self, token: RefreshInput):
        token_dict = token.model_dump()
        token = await self.token_repo.get_one(filters=token_dict)
        return token