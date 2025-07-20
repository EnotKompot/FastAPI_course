from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.api.dependencies import DBDep, UserIDDep

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("",
            summary="Показывает все имеющиеся записи по бронированию"
            )
@cache(expire=60)
async def get_all_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get("/me",
            summary="Показывает все записи по бронированию для текущего пользователя"
            )
@cache(expire=60)
async def get_my_bookings(
        user_id: UserIDDep,
        db: DBDep
):
    return await db.bookings.get_all_filtered(user_id=user_id)


@router.post('',
             summary="Добавляет бронирование для текущего пользователя"
             )
async def add_booking(
        user_id: UserIDDep,
        db: DBDep,
        booking_data: BookingAddRequestSchema,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(
        _booking_data,
        hotel_id=hotel.id
    )
    await db.commit()
    return {"success": True, "data": booking}
