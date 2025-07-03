from datetime import date

from fastapi import Query, APIRouter, Body

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
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(example="2025-06-14"),
        date_to: date = Query(example="2025-06-19"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to
    )


@router.get(
    "/{hotel_id}",
    summary = "Возвращает запись о конкретном отеле",
)
async def get_hotel(
        hotel_id: int,
        db: DBDep,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Создает запись о новом отеле",
)
async def add_hotel(
        db: DBDep,
        hotel_data: HotelAddSchema = Body(openapi_examples={
            "1": {"summary": "Сочи", "value":{
                "title": "Отель 5 звезд у моря",
                "location": "Сочи, ул. Морская, 7"
            }},
            "2": {"summary": "Дубай", "value":{
                "title": "Элитный вид",
                "location": "Дубай, ул. Шейха-Перешейха, 123"
            }}
        }),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"success": True, "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Редактирует все данные в записи отеля",
)
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelAddSchema,
        db: DBDep
):
    await db.hotels.update(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"success": True, "message": "Hotel updated successfully"}


@router.patch(
    "/{hotel_id}",
    summary="Редактирует часть данных в записи отеля",
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCHSchema,
        db: DBDep
):
    await db.hotels.update_particular(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"success": True, "message": "Hotel updated successfully"}


@router.delete(
    "/{hotel_id}",
    summary="Удаляет запись об отеле",
)
async def del_hotel(
        hotel_id: int,
        db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"success": True}