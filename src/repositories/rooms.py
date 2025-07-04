from datetime import date

from fastapi import HTTPException

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomSchema, RoomPATCHSchema
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.hotels import HotelsRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = RoomSchema

    async def is_hotel_exist(self, hotel_id: int) -> None:
        '''
        Данная функия используется для проверки наличия отеля с указанным ID.
        Позволяет вызывать ошибку при попытке работы с неверным ID отеля
        '''
        result = await HotelsRepository(self.session).get_one_or_none(id=hotel_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Hotel ID not found")

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        awailable_rooms = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )
        return await self.get_all_filtered(RoomsORM.id.in_(awailable_rooms))



    async def add(self, data):
        await self.is_hotel_exist(data.hotel_id)
        return await super().add(data)


    async def delete(self, **filter_by) -> None:
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().delete(**filter_by)


    async def update(self, data, **filter_by):
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().update(data, **filter_by)


    async def update_particular(self, data: RoomPATCHSchema, exclude_unset=False, **filter_by):
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().update_particular(data=data, exclude_unset=exclude_unset, **filter_by)