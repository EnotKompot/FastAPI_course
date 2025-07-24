from exceptions import ObjectNotFoundException, RoomNotFoundException
from schemas.hotels import HotelSchema
from schemas.rooms import RoomSchema
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base_service import BaseService


class BookingsService(BaseService):
    async def add_new_booking(self, user_id: int, booking_data: BookingAddRequestSchema):
        try:
            room: RoomSchema = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel: HotelSchema = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAddSchema(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(exclude_unset=True),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_current_user_bookings(self, user_id: int):
        return await self.db.bookings.get_all_filtered(user_id=user_id)