from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = BookingSchema