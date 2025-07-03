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

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
        query = select(HotelsORM)
        if title:
            query = (
                query
                .where(HotelsORM.title.ilike(f"%{title.strip()}%"))
            )
        if location:
            query = (
                query
                .where(HotelsORM.location.ilike(f"%{location.strip()}%"))
            )

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [HotelSchema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date
    ):
        awailable_rooms = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to
        )
        hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(awailable_rooms))
        )
        return await self.get_all_filtered(self.model.id.in_(hotels_ids))