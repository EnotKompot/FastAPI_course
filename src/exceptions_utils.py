from datetime import date

from src.api.dependencies import DBDep
from src.exceptions import DatefromOverDatetoException, ObjectNotFoundException, RoomNotFoundException


def validate_datefrom_dateto(*, date_from: date, date_to: date):
    if date_from > date_to:
        raise DatefromOverDatetoException


async def check_room_id_exist(db: DBDep, room_id: int):
    try:
        room = await db.rooms.get_one_with_rels(id=room_id)
    except ObjectNotFoundException as ex:
        raise RoomNotFoundException from ex
    return room