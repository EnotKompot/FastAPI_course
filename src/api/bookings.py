from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from exceptions import DatefromOverDatetoException
from src.exceptions import ObjectNotFoundException, RoomNotFoundException, NoFreeRoomException
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.api.dependencies import DBDep, UserIDDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Показывает все имеющиеся записи по бронированию")
@cache(expire=60)
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Показывает все записи по бронированию для текущего пользователя")
@cache(expire=60)
async def get_my_bookings(user_id: UserIDDep, db: DBDep):
    return await db.bookings.get_all_filtered(user_id=user_id)


@router.post("", summary="Добавляет бронирование для текущего пользователя")
async def add_booking(
    user_id: UserIDDep,
    db: DBDep,
    booking_data: BookingAddRequestSchema,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=RoomNotFoundException.status_code, detail=RoomNotFoundException.detail)
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except NoFreeRoomException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except DatefromOverDatetoException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    await db.commit()
    return {"success": True, "data": booking}