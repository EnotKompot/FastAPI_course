from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime

from src.database import BaseModel


class UsersORM(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=200))
    hashed_password: Mapped[str] = mapped_column((String(length=200)))
    first_name: Mapped[str | None] = mapped_column(String(length=100))
    last_name: Mapped[str | None] = mapped_column(String(length=100))
    nickname: Mapped[str] = mapped_column(String(length=100))