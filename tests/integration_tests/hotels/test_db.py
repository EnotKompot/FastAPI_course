from src.schemas.hotels import HotelAddSchema
from src.utils.db_manager import DBManager
from src.utils.database import new_session_null_pool


async def test_add_hotel():
    hotel_add = HotelAddSchema(title="Hotel 5 stars", location="Sochi")

    async with DBManager(session_factory=new_session_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_add)
        await db.commit()
        print(f"{new_hotel_data=}")