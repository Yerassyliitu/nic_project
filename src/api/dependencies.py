from src.repositories.user_game import UserGameRepository
from src.services.user_game import UserGameService
from src.repositories.match import MatchRepository
from src.services.match import MatchService
from src.repositories.role import RoleRepository
from src.services.role import RoleService
from src.repositories.user import UserRepository
from src.services.user import UserService


def user_service():
    return UserService(UserRepository())



def role_service():
    return RoleService(RoleRepository())


def match_service():
    return MatchService(MatchRepository())


def user_game_service():
    return UserGameService(UserGameRepository())