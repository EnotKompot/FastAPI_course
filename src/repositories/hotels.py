from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsORM
from src.repositories.utils import rooms_ids_for_booking
from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = HotelSchema


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            offset: int,
            limit: int = 5,
    ):
        awailable_rooms = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to
        )

        hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(awailable_rooms))
            .limit(limit)
            .offset(offset)
        )

        return await self.get_all_filtered(self.model.id.in_(hotels_ids))