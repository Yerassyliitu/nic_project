from typing import Optional

from pydantic import BaseModel


class UserGameRead(BaseModel):
    id: int
    user_id: Optional[int]
    game_id: Optional[int]


class UserGameCreate(BaseModel):
    user_id: int
    game_id: int
