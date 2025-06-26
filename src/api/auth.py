from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import new_session
from src.repositories.auth import UsersRepository
from src.schemas.auth import UserAdd, UserRequestAdd

router = APIRouter(
    prefix='/auth',
    tags=["Авторизация и аутентификация"]
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


@router.post('/register')
async def registry_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
        nickname=data.nickname
    )
    async with new_session() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"success": True}