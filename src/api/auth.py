from fastapi import APIRouter, HTTPException, Response
from fastapi_cache.decorator import cache

from src.api.dependencies import UserIDDep, DBDep
from src.schemas.auth import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=["Авторизация и аутентификация"]
)


@router.post('/register')
async def registry_user(
        data: UserRequestAdd,
        db: DBDep
):
    if await db.users.user_exists(email=data.email) is True:
        raise HTTPException(status_code=409, detail=f'User with email {data.email} already exists. Use another email.')

    await db.users.add(data)
    await db.commit()
    return {"success": True}


@router.post('/login')
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep
):

    user = await db.users.get_user_with_hashed_password(email=data.email)
    if user is None:
        raise HTTPException(status_code=401, detail=f'User with email {data.email} does not exist.')
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect password.')

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get('/me')
@cache(expire=60)
async def get_me(
        user_id: UserIDDep,
        db: DBDep
):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout") # Used to keep cache clear of user sensetive data
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")  # Unsensetive for invalid token value
    return {"success": True, "message": "Logged out"}