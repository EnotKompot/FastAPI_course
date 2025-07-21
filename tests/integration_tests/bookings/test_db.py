from datetime import date

from src.schemas.bookings import BookingAddSchema



async def test_booking_crud(get_db_null_pool, test_register_user):
    room_id = (await get_db_null_pool.rooms.get_all())[0].id
    user_id = (await get_db_null_pool.users.get_all())[0].id

    # Add data to bookings
    booking_add = BookingAddSchema(
        room_id = room_id,
        user_id = user_id,
        date_from = date(year=2024, month=12, day=25),
        date_to = date(year=2025, month=1, day=11),
        price = 1000,
    )
    booking_add_query = await get_db_null_pool.bookings.add(booking_add)
    assert isinstance(booking_add_query, BookingAddSchema)

    # Get data of booking
    booking_get_query = await get_db_null_pool.bookings.get_one_or_none(id=booking_add_query.id)
    assert booking_get_query is not None
    assert booking_get_query.room_id == room_id
    assert booking_get_query.user_id == user_id

    # Delete data of booking
    await get_db_null_pool.bookings.delete(id=booking_add_query.id)
    # assert await get_db_null_pool.bookings.get_all() == []
    await get_db_null_pool.commit()