from fastapi import HTTPException

from datetime import date


class BelsHotelException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BelsHotelException):
    detail = 'Объект не найден'


class AllRoomsAreBookedException(BelsHotelException):
    detail = 'Не осталось свободных номеров'

class UserAlreadyExists(BelsHotelException):
    detail = 'Пользователь уже существует!'

class UserNotExists(BelsHotelException):
    detail = 'Пользователь не найден!'

class IncorrectPassword(BelsHotelException):
    detail = 'неверный пароль!'


class RoomNotFoundException(BelsHotelException):
    detail = "Номер не найден"


class HotelNotFoundException(BelsHotelException):
    detail = "Отель не найден"


class BelsHotelHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class HotelNotFoundHTTPException(BelsHotelHTTPException):
    status_code = 404
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(BelsHotelHTTPException):
    status_code = 404
    detail = 'номер не найден'


class UserAlreadyExistsExceptionHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Такой пользователь уже существует!'


class UserNotExistsHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Пользователь не найден!'

class IncorrectPasswordhttpException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Неверный пароль!'

class AllRoomsAreBookedHTTPException(BelsHotelException):
    detail = 'Не осталось свободных номеров'


class UserAlreadyExistsException(BelsHotelHTTPException):
    detail = 'Пользователь сущетсвует'