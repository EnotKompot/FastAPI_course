from src.schemas.facilities import FacilitySchema
from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilitySchema