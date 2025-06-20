from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import BaseModel


class RoomsORM(BaseModel):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[str | None]
    description: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]

