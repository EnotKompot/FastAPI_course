from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    nickname: str
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    nickname: str
    hashed_password: str

class User(BaseModel):
    id: int
    nickname: str
    email: str

class UserWithHashedPassword(User):
    email: EmailStr
    nickname: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)