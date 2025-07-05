from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.utils.database import BaseModel


class FacilitiesORM(BaseModel):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=100))

    rooms: Mapped[list["RoomsORM"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )


class RoomFacilitiesORM(BaseModel):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))