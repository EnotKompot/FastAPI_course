from fastapi import Query, APIRouter, Body

from dependencies import PaginationDep
from schemas.schemas_hotels import HotelSchema, HotelPATCHSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 8, 'title': 'Kiev', "name": "Velikie-holmi"},
]


@router.get(
    "",
    summary="Возвращает запись о конкретном отеле",
)
def get_hotel(
        pagination: PaginationDep,
        id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Город отеля"),
):
    result = []

    for hotel in hotels:
        if ((id is not None and hotel["id"] != id)
                or (title is not None and hotel["title"] != title)):
            continue
        result.append(hotel)

    paginate_start = (pagination.page - 1) * pagination.per_page
    paginate_end = paginate_start + pagination.per_page
    return result[paginate_start:paginate_end]


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
def add_hotel(hotel_data: HotelSchema = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель 5 звезд у моря",
        "name": "sochi_u_morya"
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Дубай элитный вид",
        "name": "dubai-v-nebe"
    }}
})
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]['id'] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )
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