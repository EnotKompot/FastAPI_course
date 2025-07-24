from fastapi import HTTPException


class DefaultException(Exception):
    detail: str = "Base exception message"


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(DefaultException):
    '''Exception for database objects that can not be found'''

    detail = "Object not found"

class RoomNotFoundException(ObjectNotFoundException):

    detail = 'Room not found. Please, try another parameters to search'


class NoFreeRoomException(DefaultException):
    detail = "There a no free rooms to book."


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found. Please, try another parameters to search"


class DatefromOverDatetoException(DefaultException):
    detail = "Start of booking over end of booking. Please input correct date range"


class UserNotFoundException(ObjectNotFoundException):
    detail = "User not found. Please login first"


class InvalidTokenException(DefaultException):
    detail = "Invalid token. Please login with correct personal data"


class DefaultHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundHTTPException(DefaultHTTPException):
    status_code = 400
    detail = 'Room not found. Please, try another parameters to search'


class NoFreeRoomHTTPException(DefaultHTTPException):
    status_code = 404
    detail = "There are no free rooms to book."


class HotelNotFoundHTTPException(DefaultHTTPException):
    status_code = 400
    detail = "Hotel not found. Please, try another parameters to search"


class DatefromOverDatetoHTTPException(DefaultHTTPException):
    status_code = 400
    detail = "Start of booking over end of booking. Please input correct date range"