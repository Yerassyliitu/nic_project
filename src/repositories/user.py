from src.models.user import User
from .repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User


# api_key: E0987ED7404BB5DEA37F13BD20D41758
# domen: 6561199096464451