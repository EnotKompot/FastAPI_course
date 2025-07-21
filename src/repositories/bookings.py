from fastapi import HTTPException
from datetime import date

from sqlalchemy import select

from repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAddSchema
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsORM


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .select_from(BookingsORM)
            .filter(BookingsORM.date_to == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]


    async def add_booking(self, data: BookingAddSchema, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id not in rooms_ids_to_book:
            raise HTTPException(status_code=404, detail="Where a no free rooms left")

        new_booking = await self.add(data)
        return new_booking
