from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.bookings import BookingAddRequestSchema
from src.services.bookings import BookingsService
from exceptions import NoFreeRoomHTTPException, NoFreeRoomException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Показывает все имеющиеся записи по бронированию")
@cache(expire=60)
async def get_all_bookings(db: DBDep):
    bookings = await BookingsService(db).get_bookings()
    return {"success": True, "data_list": bookings}


@router.get("/me", summary="Показывает все записи по бронированию для текущего пользователя")
@cache(expire=60)
async def get_my_bookings(user_id: UserIDDep, db: DBDep):
    user_bookings = await BookingsService(db).get_current_user_bookings(user_id)
    return {"success": True, "data_list": user_bookings}


@router.post("", summary="Добавляет бронирование для текущего пользователя")
async def add_booking(
    user_id: UserIDDep,
    db: DBDep,
    booking_data: BookingAddRequestSchema,
):
    try:
        new_booking = await BookingsService(db).add_new_booking(user_id, booking_data)
    except NoFreeRoomException:
        raise NoFreeRoomHTTPException
    return {"success": True, "data": new_booking}
