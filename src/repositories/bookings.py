from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper