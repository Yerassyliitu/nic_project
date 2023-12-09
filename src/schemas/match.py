from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MatchCreate(BaseModel):
    user1_id: int
    user2_id: int
    status: bool = False


class MatchRead(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    status: bool = False
    created_at: Optional[datetime]


class MatchEdit(BaseModel):
    user1_id: int
    user2_id: int
    status: bool = False
    created_at: Optional[datetime]