from typing import Annotated
from fastapi import Depends, HTTPException, Request

from pydantic import BaseModel, Field

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int, Field(default=1, ge=1)]
    per_page: Annotated[int, Field(default=3, ge=1, lt=50)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="You are not authenticated. Provide token.")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data.get('user_id')

UserIDDep = Annotated[int, Depends(get_current_user_id)]
