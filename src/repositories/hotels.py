from datetime import date

from sqlalchemy import select, func

from exceptions import DatefromOverDatetoException
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelDataMapper


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        location: str,
        title: str,
        date_from: date,
        date_to: date,
        offset: int,
        limit: int = 5,
    ):
        if date_from > date_to:
            raise DatefromOverDatetoException

        awailable_rooms = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids = (
            select(RoomsORM.hotel_id).select_from(RoomsORM).filter(RoomsORM.id.in_(awailable_rooms))
        )

        query = select(self.model).filter(self.model.id.in_(hotels_ids))

        if title is not None:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if location is not None:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]