from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.models.hotels import HotelsORM
from src.repositories.hotels import HotelsRepository
from src.database import new_session, engine
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelSchema, HotelPATCHSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)



@router.get(
    "",
    summary="Возвращает запись о конкретном отеле",
)
async def get_hotel(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with new_session() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.delete(
    "/{hotel_id}",
    summary="Удаляет запись об отеле",
)
async def del_hotel(
        id: int
):
    async with new_session() as session:
        await HotelsRepository(session).delete(id=id)
        await session.commit()


@router.post(
    "",
    summary="Создает запись о новом отеле",
)
async def add_hotel(hotel_data: HotelSchema = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель 5 звезд у моря",
        "location": "Сочи, ул. Морская, 7"
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Элитный вид",
        "location": "Дубай, ул. Шейха-Перешейха, 123"
    }}
})
):
    async with new_session() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"success": True, "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Редактирует все данные в записи отеля",
)
async def update_hotel(hotel_id: int, hotel_data: HotelSchema):
    async with new_session() as session:
        await HotelsRepository(session).update(data=hotel_data,
                                               id=hotel_id)
        await session.commit()
    return {"success": True, "message": "Hotel updated successfully"}


@router.patch(
    "/{hotel_id}",
    summary="Редактирует часть данных в записи отеля",
)
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCHSchema
):
    global hotels

    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"success": True, "message": "Hotel updated successfully"}