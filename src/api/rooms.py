from fastapi import APIRouter, HTTPException, Query, Body

from src.schemas.rooms import RoomPATCHSchema
from src.api.dependencies import PaginationDep
from src.schemas.rooms import RoomAddSchema
from src.database import new_session
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Номера  "])



@router.get("/{hotel_id}/rooms")
async def get_rooms(
        pagination: PaginationDep,
        hotel_id: int,
        title: str | None = Query(default=None, description="Название номера"),
        description: str | None = Query(default=None, description="Описание номера"),
):
    per_page = pagination.per_page or 10
    async with new_session() as session:
        query = await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

    if len(query) == 0:
        raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} has no rooms")
    return query


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        hotel_id: int,
        room_id: int
):
    async with new_session() as session:
        query = await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id
        )

    if query is None:
        raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} has no room with id {room_id}")
    return query


@router.post("/{hotel_id}/rooms/{room_id}")
async def add_room(room: RoomAddSchema = Body(openapi_examples={
    "1": {"summary": "Double bed", "value":{
        "hotel_id": 15,
        "title": "Double bed room",
        "description": "Просторная комната с двуспальной кроватью",
        "price": 2000,
        "quantity": 10
    }},
    "2": {"summary": "View to sea", "value":{
        "hotel_id": 16,
        "title": "King view to the sea",
        "description": "Комната с панорамными окнами и видом на море",
        "price": 5000,
        "quantity": 15
    }}
})):
    async with new_session() as session:
        await RoomsRepository(session).add(room)
        await session.commit()
    return {"success": True, "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int
):
    async with new_session() as session:
        await RoomsRepository(session).delete(
            hotel_id=hotel_id,
            room_id=room_id
        )
        await session.commit()
    return {"success": True}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data:RoomAddSchema):
    async with new_session() as session:
        await RoomsRepository(session).update(
            data=room_data,
            hotel_id=hotel_id,
            id=room_id,
        )
        await session.commit()
    return {"success": True}



@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCHSchema):
    async with new_session() as session:
        await RoomsRepository(session).update_particular(
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id,
            data=room_data
        )
        await session.commit()
    return {"success": True}