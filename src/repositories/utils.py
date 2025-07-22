from datetime import date

from sqlalchemy import select, func

from schemas.facilities import RoomFacilityAddSchema
from schemas.rooms import RoomAddRequestSchema, RoomPatchRequestSchema
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )
    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    hotel_rooms_ids = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id is not None:
        hotel_rooms_ids = hotel_rooms_ids.filter_by(hotel_id=hotel_id)
    hotel_rooms_ids = hotel_rooms_ids.subquery(name="hotel_rooms_ids")

    awailable_rooms = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0, rooms_left_table.c.room_id.in_(hotel_rooms_ids))
    )
    return awailable_rooms


async def update_room_facilities(
    room_id: int, data: RoomAddRequestSchema | RoomPatchRequestSchema, db
):
    current_facilities = await db.rooms_facilities.get_all_filtered(room_id=room_id)
    last_facilities = {facility.facility_id for facility in current_facilities}
    new_facilities = set(data.facilities_ids)

    remove_unused_facilities = [
        RoomFacilityAddSchema(room_id=room_id, facility_id=f_id)
        for f_id in last_facilities.difference(new_facilities)
    ]
    if remove_unused_facilities:
        await db.rooms_facilities.delete_bulk(remove_unused_facilities)
    add_new_facilities = [
        RoomFacilityAddSchema(room_id=room_id, facility_id=f_id)
        for f_id in new_facilities.difference(last_facilities)
    ]
    if add_new_facilities:
        await db.rooms_facilities.add_bulk(add_new_facilities)
