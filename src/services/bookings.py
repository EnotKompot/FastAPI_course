from repositories.mappers.mappers import BookingDataMapper
from src.api.dependencies import UserIDDep
from src.exceptions import NoFreeRoomException
from src.exceptions_utils import check_room_id_exist, validate_datefrom_dateto
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base_service import BaseService


class BookingsService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()


    async def get_current_user_bookings(self, user_id: int):
        return await self.db.bookings.get_all_filtered(user_id=user_id)


    async def add_new_booking(self, user_id: UserIDDep, booking_data: BookingAddRequestSchema,
):
        room = await check_room_id_exist(db=self.db, room_id=booking_data.room_id)
        validate_datefrom_dateto(date_from=booking_data.date_from, date_to=booking_data.date_to)
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAddSchema(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except:
            raise NoFreeRoomException
        await self.db.commit()
        return booking