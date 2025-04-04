from fastapi import HTTPException


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



class BelsHotelHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BelsHotelHTTPException):
    status_code = 404
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(BelsHotelHTTPException):
    status_code = 404
    detail = 'номер не найден'