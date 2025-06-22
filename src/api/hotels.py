from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from models.hotels import HotelsORM
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
        query = select(HotelsORM)
        if title:
            query = query.filter_by(title=title)
        if location:
            query = (
                query
                .where(HotelsORM.location.ilike(f"%{location}%"))
            )

        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        return result.scalars().all()


    # paginate_start = (pagination.page - 1) * pagination.per_page
    # paginate_end = paginate_start + pagination.per_page


@router.delete(
    "/{hotel_id}",
    summary="Удаляет запись об отеле",
)
def del_hotel(
        hotel_id: int
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotels.remove(hotel)
    return {"success": True, "message": f"Hotel with id = {hotel_id} deleted successfully"}


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
        add_hotel_stmt = (
            insert(HotelsORM)
            .values(**hotel_data.model_dump())
        )
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"success": True, "message": "Hotel added successfully"}


@router.put(
    "/{hotel_id}",
    summary="Редактирует все данные в записи отеля",
)
def update_hotel(hotel_id: int, hotel_data: HotelSchema):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_data.hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
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