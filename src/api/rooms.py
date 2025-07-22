from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from exceptions import DatefromOverDatetoException
from src.api.dependencies import DBDep
from src.exceptions import RoomNotFoundException, ObjectNotFoundException, HotelNotFoundException
from src.repositories.utils import update_room_facilities
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import (
    RoomAddSchema,
    RoomAddRequestSchema,
    RoomPatchRequestSchema,
    RoomPatchSchema,
)

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
@cache(expire=60)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2025-06-14"),
    date_to: date = Query(example="2025-06-19"),
):
    try:
        query = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return query
    except DatefromOverDatetoException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)

@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=60)
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        query = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        return query
    except ObjectNotFoundException:
        raise HTTPException(status_code=RoomNotFoundException.status_code, detail=RoomNotFoundException.detail)


@router.post("/{hotel_id}/rooms/")
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequestSchema,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=HotelNotFoundException.status_code, detail=HotelNotFoundException.detail)
    _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await db.rooms.delete(hotel_id=hotel_id, room_id=room_id)
    await db.commit()
    return {"success": True}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequestSchema,
    db: DBDep,
):
    _room = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
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
        hotel_id=hotel_id, id=room_id, **room_data.model_dump(exclude_unset=True)
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