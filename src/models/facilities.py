from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

from src.utils.database import BaseModel


class FacilitiesORM(BaseModel):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=100))


class RoomFacilitiesORM(BaseModel):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(unique=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)