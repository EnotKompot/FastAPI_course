from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BookingAddRequestSchema):
    user_id: int
    price: int


class BookingSchema(BookingAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)