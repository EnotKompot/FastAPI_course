from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import RoomFacilitySchema
from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacilitySchema
