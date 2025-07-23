from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundException, DatefromOverDatetoException, \
    DatefromOverDatetoHTTPException
from src.services.hotels import HotelsService
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAddSchema, HotelPATCHSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    "",
    summary="Возвращает данные обо всех отелях",
)
@cache(expire=60)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str = None,
    location: str = None,
    date_from: date = Query(example="2025-06-14"),
    date_to: date = Query(example="2025-06-19"),
):
    try:
        hotels = await HotelsService(db).get_hotels(
            pagination=pagination,
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
        )
        return {"success": True, "data_list": hotels}
    except DatefromOverDatetoException:
        raise DatefromOverDatetoHTTPException

@router.get(
    "/{hotel_id}",
    summary="Возвращает запись о конкретном отеле",
)
@cache(expire=60)
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=HotelNotFoundException.status_code, detail=HotelNotFoundException.detail)

@router.post(
    "",
    summary="Создает запись о новом отеле",
)
async def add_hotel(
    db: DBDep,
    hotel_data: HotelAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель 5 звезд у моря", "location": "Сочи, ул. Морская, 7"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Элитный вид", "location": "Дубай, ул. Шейха-Перешейха, 123"},
            },
        }
    ),
):
    hotel = await HotelsService(db).add_hotel(hotel_data)
    return {"success": True, "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Редактирует все данные в записи отеля",
)
async def update_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DBDep):
    await HotelsService(db).update_hotel(hotel_id, hotel_data)
    return {"success": True, "message": "Hotel updated successfully"}


@router.patch(
    "/{hotel_id}",
    summary="Редактирует часть данных в записи отеля",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCHSchema, db: DBDep):
    await HotelsService(db).patch_hotel(hotel_id, hotel_data)
    return {"success": True, "message": "Hotel updated successfully"}


@router.delete(
    "/{hotel_id}",
    summary="Удаляет запись об отеле",
)
async def del_hotel(
    hotel_id: int,
    db: DBDep,
):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"success": True}
