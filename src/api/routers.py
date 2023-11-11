from .role import role_router
from .user import user_router

all_routers = [
    user_router,
    role_router,
]