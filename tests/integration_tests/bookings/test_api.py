import pytest
from sqlalchemy import delete

from src.models import BookingsORM
from src.utils.db_manager import DBManager


@pytest.mark.parametrize(
    "hotel_id, room_id, date_from, date_to, status_code",
    [
        (1, 1, "2024-12-10", "2024-12-25", 200),
        (1, 1, "2024-12-11", "2024-12-26", 200),
        (1, 1, "2024-12-12", "2024-12-27", 200),
        (1, 1, "2024-12-13", "2024-12-28", 200),
        (1, 1, "2024-12-14", "2024-12-29", 200),
        (1, 1, "2024-12-15", "2024-12-29", 404),
        (1, 1, "2024-12-30", "2024-12-31", 200),
    ],
)
async def test_add_booking(
    hotel_id,
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["success"] is True
        assert "data" in res


@pytest.fixture(scope="session")
async def clear_bookings(db: DBManager):
    async with db.session.begin():
        await db.session.execute(delete(BookingsORM))
    yield


@pytest.mark.parametrize(
    "hotel_id, room_id, date_from, date_to, bookings_count",
    [
        (1, 2, "2024-12-10", "2024-12-25", 1),
        (1, 2, "2024-12-11", "2024-12-26", 2),
        (1, 2, "2024-12-12", "2024-12-27", 3),
    ],
)
async def test_add_and_get_bookings(
    clear_bookings,
    hotel_id,
    room_id,
    date_from,
    date_to,
    bookings_count,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "hotel_id": hotel_id,
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200
    bookings = await authenticated_ac.get(
        "/bookings/me",
    )
    assert len(bookings.json()) == bookings_count
