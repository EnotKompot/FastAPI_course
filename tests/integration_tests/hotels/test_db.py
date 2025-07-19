from src.schemas.hotels import HotelAddSchema


async def test_add_hotel(db):
    hotel_add = HotelAddSchema(title="Hotel 5 stars", location="Sochi")
    new_hotel_data = await db.hotels.add(hotel_add)
    await db.commit()
    print(f"{new_hotel_data=}")