from sqlalchemy import or_, and_

from src.schemas.match import MatchCreate

from src.repositories.repository import AbstractRepository


class MatchService:
    def __init__(self, match_repo: AbstractRepository):
        self.match_repo: AbstractRepository = match_repo

    async def add_match(self, match: MatchCreate):
        match_dict = match.model_dump()
        match_id = await self.match_repo.add_one(data=match_dict)
        return match_id

    async def get_matches_by_one_id(self, id):
        match = await self.match_repo.get_all(user1_id=id)
        if not match:
            match = await self.match_repo.get_all(user2_id=id)
        return match

    async def get_match_by_two_id(self, user1_id, user2_id):
        match = await self.match_repo.get_one(user1_id=user1_id, user2_id=user2_id)
        if not match:
            match = await self.match_repo.get_one(user1_id=user2_id, user2_id=user1_id)
        return match

    async def get_matches(self):
        matches = await self.match_repo.get_all()
        return matches

    async def edit_match(self, user1_id, user2_id, status):
        existing_match = await self.match_repo.get_one(user1_id=user1_id, user2_id=user2_id)
        if not existing_match:
            existing_match = await self.match_repo.get_one(user1_id=user2_id, user2_id=user1_id)
        if existing_match:
            edited_match = await self.match_repo.edit_one(data={"status": status},
                                                          user1_id=existing_match.user1_id,
                                                          user2_id=existing_match.user2_id, )
            return edited_match
        else:
            return None

    async def delete_match(self, user1_id, user2_id):
        existing_match = await self.match_repo.get_one(user1_id=user1_id, user2_id=user2_id)

        if not existing_match:
            existing_match = await self.match_repo.get_one(user1_id=user2_id, user2_id=user1_id)

        if existing_match:
            edited_match = await self.match_repo.delete_one(user1_id=existing_match.user1_id,
                                                            user2_id=existing_match.user2_id)
            return edited_match
        else:
            return None
