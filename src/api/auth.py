from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIDDep
from src.database import new_session
from src.repositories.auth import UsersRepository
from src.schemas.auth import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=["Авторизация и аутентификация"]
)


@router.post('/register')
async def registry_user(
        data: UserRequestAdd,
):

    async with new_session() as session:
        if await UsersRepository(session).user_exists(email=data.email) is True:
            raise HTTPException(status_code=409, detail=f'User with email {data.email} already exists. Use another email.')
        else:
            await UsersRepository(session).add(data)
            await session.commit()
            return {"success": True}


@router.post('/login')
async def login_user(
        data: UserRequestAdd,
        response: Response,
):

    async with new_session() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if user is None:
            raise HTTPException(status_code=401, detail=f'User with email {data.email} does not exist.')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail=f'Incorrect password.')
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.get('/me')
async def get_me(
        user_id: UserIDDep
):

    async with new_session() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user
