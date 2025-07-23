from fastapi import HTTPException


class DefaultException(Exception):
    status_code: int = 500
    detail: str = "Base exception message"


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(DefaultException):
    '''Exception for database objects that can not be found'''
    status_code = 404
    detail = "Object not found"

class RoomNotFoundException(ObjectNotFoundException):
    status_code = 400
    detail = 'Room not found. Please, try another parameters to search'


class RoomNotFoundHTTPException(HTTPException):
    status_code = 400
    detail = 'Room not found. Please, try another parameters to search'


class NoFreeRoomException(DefaultException):
    status_code = 400
    detail = "There a no free rooms to book."


class HotelNotFoundException(ObjectNotFoundException):
    status_code = 400
    detail = "Hotel not found. Please, try another parameters to search"


class HotelNotFoundHTTPException(HTTPException):
    status_code = 400
    detail = "Hotel not found. Please, try another parameters to search"


class DatefromOverDatetoException(DefaultException):
    status_code = 400
    detail = "Start of booking over end of booking. Please input correct date range"


class DatefromOverDatetoHTTPException(HTTPException):
    status_code = 400
    detail = "Start of booking over end of booking. Please input correct date range"

class UserNotFoundException(ObjectNotFoundException):
    status_code = 400
    detail = "User not found. Please login first"


class InvalidTokenException(DefaultException):
    status_code = 401
    detail = "Invalid token. Please login with correct personal data"