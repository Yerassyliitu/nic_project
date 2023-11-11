from pydantic import BaseModel


class Login(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class LogOut(BaseModel):
    access_token: str


class RefreshInput(BaseModel):
    refresh_token: str


class RefreshOutput(BaseModel):
    access_token: str
    token_type: str