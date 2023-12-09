from typing import Optional
from pydantic import EmailStr, BaseModel


class GameRead(BaseModel):
    id: int
    app_id: int
    name: str
    playtime_2weeks: Optional[int] = None
    playtime_forever: Optional[int] = None
    img_icon_url: str


class GameCreate(BaseModel):
    app_id: int
    name: str
    playtime_2weeks: Optional[int] = None
    playtime_forever: Optional[int] = None
    img_icon_url: str

