from fastapi import APIRouter, HTTPException


from src.database import new_session
from src.repositories.auth import UsersRepository
from src.schemas.auth import UserRequestAdd

router = APIRouter(
    prefix='/auth',
    tags=["Авторизация и аутентификация"]
)


@router.post('/register')
async def registry_user(
        data: UserRequestAdd
):

    async with new_session() as session:
        if await UsersRepository(session).user_exists(email=data.email) is True:
            raise HTTPException(status_code=422, detail='User already exists')
        else:
            await UsersRepository(session).add(data)
            await session.commit()
            return {"success": True}