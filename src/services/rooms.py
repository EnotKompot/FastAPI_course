from datetime import date

from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.exceptions_utils import validate_datefrom_dateto
from src.repositories.utils import update_room_facilities
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import RoomAddSchema, RoomAddRequestSchema, RoomPatchRequestSchema, RoomPatchSchema
from src.services.base_service import BaseService


class RoomsService(BaseService):
    async def get_rooms(self, hotel_id: int, date_from: date, date_to: date):
        validate_datefrom_dateto(date_from=date_from, date_to=date_to)
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        query = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return query


    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)


    async def add_room(self, hotel_id: int, room_data: RoomAddRequestSchema):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room


    async def delete_room(self, hotel_id: int, room_id: int):
        await self.db.rooms.delete(hotel_id=hotel_id, room_id=room_id)
        await self.db.commit()


    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequestSchema):
        _room = RoomPatchSchema(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.update(
            data=_room,
            hotel_id=hotel_id,
            id=room_id,
        )
        await update_room_facilities(data=room_data, room_id=room_id, db=self.db)
        await self.db.commit()
        return _room


    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequestSchema):
        _room = RoomPatchSchema(
            hotel_id=hotel_id, id=room_id, **room_data.model_dump(exclude_unset=True)
        )
        await self.db.rooms.update_particular(
            data=_room,
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True,
        )
        await update_room_facilities(data=room_data, room_id=room_id, db=db)
        await self.db.commit()