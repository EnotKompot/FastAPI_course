from fastapi import APIRouter, Request

from schemas.bookings import BookingSchema
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.api.dependencies import DBDep, UserIDDep

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("",
            summary="Показывает все имеющиеся записи по бронированию"
            )
async def get_all_bookings(
        db: DBDep
):
    return await db.bookings.get_all()


@router.get("/me",
            summary="Показывает все записи по бронированию для текущего пользователя"
            )
async def get_my_bookings(
        user_id: UserIDDep,
        db: DBDep
):
    return await db.bookings.get_all_filtered(user_id=user_id)


@router.post('',
             summary="Добавляет бронирование для текущего пользователя"
             )
async def add_booking(
        booking: BookingAddRequestSchema,
        db: DBDep,
        user_id: UserIDDep
):
    room_data = await db.rooms.get_one_or_none(id=booking.room_id)
    price = room_data.price * (booking.date_to - booking.date_from).days
    _booking = BookingAddSchema(
        price=price,
        user_id=user_id,
        **booking.model_dump(exclude_unset=True)
    )
    add_stmt = await db.bookings.add(_booking)
    await db.commit()
    return {"success": True, "data": add_stmt}

