from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema, RoomWithRels
from src.schemas.auth import User, UserWithHashedPassword
from src.schemas.bookings import BookingSchema
from src.schemas.facilities import FacilitySchema


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = HotelSchema


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomSchema


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User

class UserWithHashPassDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingSchema


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = FacilitySchema