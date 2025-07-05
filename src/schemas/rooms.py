from pydantic import BaseModel, Field, ConfigDict


class RoomAddRequestSchema(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=400)
    price: int = Field(gt=0, le=50000)
    quantity: int = Field(default=0, ge=0, le=20)
    facilities_ids: list[int] | None = None


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=400)
    price: int = Field(gt=0, le=50000)
    quantity: int = Field(default=0, ge=0, le=20)


class RoomSchema(RoomAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequestSchema(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=400)
    price: int | None = Field(default=None, gt=0, le=50000)
    quantity: int | None  = Field(default=None, ge=0, le=20)
    facilities_ids: list[int] | None = None


class RoomPatchSchema(BaseModel):
    hotel_id: int | None = None
    id: int
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=400)
    price: int | None = Field(default=None, gt=0, le=50000)
    quantity: int | None  = Field(default=None, ge=0, le=20)
