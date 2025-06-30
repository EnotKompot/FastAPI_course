from fastapi import APIRouter, HTTPException, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.rooms import RoomAddSchema, RoomPATCHSchema

router = APIRouter(prefix="/hotels", tags=["Номера  "])



@router.get("/{hotel_id}/rooms")
async def get_rooms(
        pagination: PaginationDep,
        db: DBDep,
        hotel_id: int,
        title: str | None = Query(default=None, description="Название номера"),
        description: str | None = Query(default=None, description="Описание номера"),
):
    per_page = pagination.per_page or 10
    query = await db.rooms.get_all(
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
        room_id: int,
        db: DBDep,
):
    query = await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id
    )

    if query is None:
        raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} has no room with id {room_id}")
    return query


@router.post("/{hotel_id}/rooms/{room_id}")
async def add_room(
        db: DBDep,
        room: RoomAddSchema = Body(openapi_examples={
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
        })
):
    room = await db.rooms.add(room)
    return {"success": True, "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
):
    await db.rooms.delete(
        hotel_id=hotel_id,
        room_id=room_id
    )
    return {"success": True}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data:RoomAddSchema,
        db: DBDep,
):
    await db.rooms.update(
        data=room_data,
        hotel_id=hotel_id,
        id=room_id,
    )
    return {"success": True}



@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCHSchema,
        db: DBDep,
):
    await db.rooms.update_particular(
        exclude_unset=True,
        hotel_id=hotel_id,
        id=room_id,
        data=room_data
    )
    return {"success": True}