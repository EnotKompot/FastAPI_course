from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from src.repositories.utils import update_room_facilities
from src.schemas.facilities import RoomFacilityAddSchema
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddSchema, RoomAddRequestSchema, RoomPatchRequestSchema, RoomPatchSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Номера"]
)



@router.get("/{hotel_id}/rooms")
@cache(expire=60)
async def get_rooms(
        # pagination: PaginationDep,
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-06-14"),
        date_to: date = Query(example="2025-06-19"),
):
    # per_page = pagination.per_page or 10
    query = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
        # limit=per_page,
        # offset=per_page * (pagination.page - 1)
    )

    # if len(query) == 0:
    #     raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} has no rooms")
    return query


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=60)
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
):
    query = await db.rooms.get_one_or_none(id=room_id)

    if query is None:
        raise HTTPException(status_code=404, detail=f"Hotel with id {hotel_id} has no room with id {room_id}")
    return query


@router.post("/{hotel_id}/rooms/")
async def add_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequestSchema,
):
    _room_data = RoomAddSchema(
        hotel_id=hotel_id,
        **room_data.model_dump()
    )
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAddSchema(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


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
    await db.commit()
    return {"success": True}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data:RoomAddRequestSchema,
        db: DBDep,
):
    _room = RoomAddSchema(
        hotel_id=hotel_id,
        **room_data.model_dump()
    )
    await db.rooms.update(
        data=_room,
        hotel_id=hotel_id,
        id=room_id,
    )
    await update_room_facilities(data=room_data, room_id=room_id, db=db)

    await db.commit()
    return {"success": True}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequestSchema,
        db: DBDep,
):
    _room = RoomPatchSchema(
        hotel_id=hotel_id,
        id=room_id,
        **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.update_particular(
        data=_room,
        hotel_id=hotel_id,
        id=room_id,
        exclude_unset=True,
    )
    await update_room_facilities(data=room_data, room_id=room_id, db=db)

    await db.commit()
    return {"success": True}