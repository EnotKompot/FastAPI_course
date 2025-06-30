from fastapi import APIRouter, Request

from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.api.dependencies import DBDep, get_token, get_current_user_id

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.post('')
async def add_booking(
        booking: BookingAddRequestSchema,
        db: DBDep,
        request: Request
):
    user_id = get_current_user_id(get_token(request))
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

