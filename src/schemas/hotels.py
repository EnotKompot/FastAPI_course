from pydantic import BaseModel, Field


class HotelAddSchema(BaseModel):
    title: str
    location: str


class HotelSchema(HotelAddSchema):
    id: int


class HotelPATCHSchema(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)
