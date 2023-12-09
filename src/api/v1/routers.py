from src.api.v1.user.match import match_router
from src.api.v1.steam.steam_games import games_router
from src.api.v1.user.auth import auth_router
from src.api.v1.user.role import role_router
from src.api.v1.steam.steam_auth import steam_auth_router
from src.api.v1.user.user import user_router

all_routers = [
    auth_router,
    user_router,
    role_router,
    steam_auth_router,
    games_router,
    match_router
]