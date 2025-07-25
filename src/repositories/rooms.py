from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions import HotelNotFoundException, ObjectNotFoundException, DatefromOverDatetoException
from src.schemas.rooms import RoomPatchSchema
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.hotels import HotelsRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def is_hotel_exist(self, hotel_id: int) -> None:
        """
        Данная функия используется для проверки наличия отеля с указанным ID.
        Позволяет вызывать ошибку при попытке работы с неверным ID отеля
        """
        try:
            await HotelsRepository(self.session).get_one(id=hotel_id)

        except ObjectNotFoundException:
            raise HotelNotFoundException


    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        if date_from > date_to:
            raise DatefromOverDatetoException
        awailable_rooms = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(awailable_rooms))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]


    async def get_one_with_rels(self, **filter_by):
        query = (select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalar_one()
        return RoomWithRelsDataMapper.map_to_domain_entity(model)


    async def add(self, data):
        await self.is_hotel_exist(data.hotel_id)
        return await super().add(data)


    async def delete(self, **filter_by) -> None:
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().delete(**filter_by)


    async def update(self, data, **filter_by):
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().update(data, **filter_by)


    async def update_particular(self, data: RoomPatchSchema, exclude_unset=False, **filter_by):
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().update_particular(data=data, exclude_unset=exclude_unset, **filter_by)
