from datetime import date

from schemas.bookings import BookingSchema
from src.schemas.bookings import BookingAddSchema



async def test_booking_crud(test_register_user, db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id

    # Add data to bookings
    booking_add = BookingAddSchema(
        room_id = room_id,
        user_id = user_id,
        date_from = date(year=2024, month=12, day=25),
        date_to = date(year=2025, month=1, day=11),
        price = 1000,
    )
    booking_add_query = await db.bookings.add(booking_add)
    assert isinstance(booking_add_query, BookingAddSchema)

    # Get data of booking
    booking_get_query = await db.bookings.get_one_or_none(id=booking_add_query.id)
    assert booking_get_query is not None
    assert booking_get_query.room_id == room_id
    assert booking_get_query.user_id == user_id
    assert booking_get_query.id == 1

    # Delete data of booking
    await db.bookings.delete(id=1)
    assert await db.bookings.get_all() == []
    await db.commit()