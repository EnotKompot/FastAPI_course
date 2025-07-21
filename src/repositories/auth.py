from pydantic import EmailStr
from sqlalchemy import insert, select

from src.repositories.mappers.mappers import UserDataMapper, UserWithHashPassDataMapper
from src.schemas.auth import UserAdd, UserRequestAdd
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.services.auth import AuthService


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper


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
            hashed_password=AuthService().hash_password(data.password),
            nickname=data.nickname
        )

        add_stmt = (
            insert(self.model)
            .values(**new_user_data.model_dump())
        )
        await self.session.execute(add_stmt)


    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashPassDataMapper.map_to_domain_entity(model)