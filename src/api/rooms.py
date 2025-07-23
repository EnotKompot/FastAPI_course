from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from exceptions import RoomNotFoundHTTPException, HotelNotFoundException, HotelNotFoundHTTPException
from services.rooms import RoomsService
from src.api.dependencies import DBDep
from src.exceptions import RoomNotFoundException
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
        rooms = await RoomsService(db).get_rooms(hotel_id, date_from, date_to)
        return {"success": True, "data_list": rooms}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=60)
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        room = await RoomsService(db).get_room(hotel_id, room_id)
        return {"success": True, "data": room}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

@router.post("/{hotel_id}/rooms/")
async def add_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequestSchema,
):
    room = await RoomsService(db).add_room(hotel_id, room_data)
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await RoomsService(db).delete_room(hotel_id, room_id)
    return {"success": True}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequestSchema,
    db: DBDep,
):
    updated_room = await RoomsService(db).update_room(hotel_id, room_id, room_data)
    return {"success": True, "data": updated_room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequestSchema,
    db: DBDep,
):
    patched_room = await RoomsService(db).patch_room(hotel_id, room_id, room_data)
    return {"success": True, "data": patched_room}