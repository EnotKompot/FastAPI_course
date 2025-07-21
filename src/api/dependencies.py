from typing import Annotated
from fastapi import Depends, HTTPException, Request

from pydantic import BaseModel, Field

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.utils.database import new_session


class PaginationParams(BaseModel):
    page: Annotated[int, Field(default=1, ge=1)]
    per_page: Annotated[int, Field(default=3, ge=1, lt=50)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail="You are not authenticated. Please login first.")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data.get('user_id')


UserIDDep = Annotated[int, Depends(get_current_user_id)]


# Контекстный менеджер для работы с базой данных
def get_db_manager():
    return DBManager(session_factory=new_session)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]