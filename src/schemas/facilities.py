from pydantic import BaseModel, Field

from schemas.rooms import RoomSchema


class FacilityAddSchema(BaseModel):
    name: str


class FacilitySchema(FacilityAddSchema):
    id: int


class RoomFacilitySchema(FacilitySchema, RoomSchema):
    room_id: int