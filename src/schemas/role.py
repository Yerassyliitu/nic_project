from typing import List
from pydantic import BaseModel


class Role(BaseModel):
    name: str
    permissions: List[str]

    class ConfigDict:
        orm_mode = True


class RoleCreate(BaseModel):
    name: str
    permissions: List[str]

    class ConfigDict:
        orm_mode = True


class RoleRead(BaseModel):
    id: int
    name: str
    permissions: List[str]

    class ConfigDict:
        orm_mode = True
