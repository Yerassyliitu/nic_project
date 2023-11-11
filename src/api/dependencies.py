from src.repositories.user import UserRepository
from src.repositories.auth import TokenRepository
from src.services.user import UserService
from src.services.auth import TokenService


def user_service():
    return UserService(UserRepository())


def token_service():
    return TokenService(TokenRepository())
