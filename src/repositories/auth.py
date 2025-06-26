from src.schemas.auth import UserAdd
from src.models.users import UsersORM
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserAdd