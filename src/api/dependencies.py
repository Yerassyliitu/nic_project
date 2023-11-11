from src.repositories.role import RoleRepository
from src.services.role import RoleService
from src.repositories.user import UserRepository
from src.repositories.auth import TokenRepository
from src.services.user import UserService
from src.services.auth import TokenService


def user_service():
    return UserService(UserRepository())


def token_service():
    return TokenService(TokenRepository())


def role_service():
    return RoleService(RoleRepository())