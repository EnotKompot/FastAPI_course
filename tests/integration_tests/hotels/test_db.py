from src.schemas.hotels import HotelAddSchema


async def test_add_hotel(get_db_null_pool):
    hotel_add = HotelAddSchema(title="Hotel 5 stars", location="Sochi")
    new_hotel_data = await get_db_null_pool.hotels.add(hotel_add)
    await get_db_null_pool.commit()
    # print(f"{new_hotel_data=}")