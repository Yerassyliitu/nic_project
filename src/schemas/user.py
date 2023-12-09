from typing import Optional
from pydantic import EmailStr, BaseModel


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    steam_id: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str



class UserEdit(BaseModel):
    email: EmailStr
    username: str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdateSteamId(BaseModel):
    steam_id: Optional[str] = None


class LoginInput(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginOutput(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshInput(BaseModel):
    refresh_token: str


class RefreshOutput(BaseModel):
    access_token: str
    token_type: str
