from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: Annotated[int, Field(default=1, ge=1)]
    per_page: Annotated[int, Field(default=3, ge=1, lt=50)]


PaginationDep = Annotated[PaginationParams, Depends()]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')