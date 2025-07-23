from datetime import date

from src.exceptions_utils import validate_datefrom_dateto
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAddSchema, HotelPATCHSchema
from src.services.base_service import BaseService


class HotelsService(BaseService):
    async def get_hotels(
            self,
            pagination: PaginationDep,
            title: str,
            location: str,
            date_from: date,
            date_to: date,
    ):
        per_page = pagination.per_page or 5
        validate_datefrom_dateto(date_from=date_from, date_to=date_to)

        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )


    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)


    async def add_hotel(self, hotel_data: HotelAddSchema):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel


    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPATCHSchema):
        await self.db.hotels.update_particular(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()


    async def update_hotel(self, hotel_id: int, hotel_data: HotelPATCHSchema):
        await self.db.hotels.update(data=hotel_data, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()