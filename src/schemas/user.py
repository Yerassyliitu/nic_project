from typing import Optional
from pydantic import EmailStr, BaseModel


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserEdit(BaseModel):
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None


