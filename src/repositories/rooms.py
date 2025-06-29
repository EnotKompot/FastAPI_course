from sqlalchemy import select
from fastapi import HTTPException

from src.repositories.hotels import HotelsRepository
from src.schemas.rooms import RoomSchema, RoomPATCHSchema
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository


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


    async def get_all(
            self,
            hotel_id: int,
            title: str,
            description: str,
            limit: int,
            offset: int,
    ):
        await self.is_hotel_exist(hotel_id)
        query = select(RoomsORM).where(RoomsORM.hotel_id == hotel_id)
        if title:
            query = query.where(RoomsORM.title == title)
        if description:
            query = query.where(RoomsORM.description == description)

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [RoomSchema.model_validate(room, from_attributes=True) for room in result.scalars().all()]


    async def get_one_or_none(self, **filter_by):
        await self.is_hotel_exist(filter_by.get("hotel_id"))
        return await super().get_one_or_none(**filter_by)


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