from sqlalchemy import insert, select

from src.api.dependencies import pwd_context
from src.schemas.auth import UserRequestAdd
from src.schemas.auth import UserAdd
from src.models.users import UsersORM
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserAdd


    async def user_exists(self, **filter_by) -> bool:
        equal_emails = (
            select(self.model)
            .filter_by(**filter_by)
        )
        equal_users = await self.session.execute(equal_emails)
        return len(equal_users.scalars().all()) > 0


    async def add(self, data: UserRequestAdd):
        new_user_data = UserAdd(
            email=data.email,
            hashed_password=pwd_context.hash(data.password),
            nickname=data.nickname
        )

        add_stmt = (
            insert(self.model)
            .values(**new_user_data.model_dump())
        )
        await self.session.execute(add_stmt)