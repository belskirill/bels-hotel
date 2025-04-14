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


class TitleNotExistsHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'title не заполнен!'

class LocationNotExistsHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'location не заполнен!'


class HotelCloseDeleteHTTPExecption(BelsHotelHTTPException):
    status_code = 409
    detail = 'Нельзя удалить отель из за связанных данных!'


class LocationhotelNotExistsHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Такой отель уже существует!'

class HotelDublicateHTTPExeption(BelsHotelHTTPException):
    status_code = 409
    detail = 'Такой отель уже существует!'



class IncorrectPasswordhttpException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Неверный пароль!'

class AllRoomsAreBookedHTTPException(BelsHotelHTTPException):
    status_code = 409
    detail = 'Не осталось свободных номеров'


class UserAlreadyExistsException(BelsHotelHTTPException):
    detail = 'Пользователь сущетсвует'


class TitleNotExists(BelsHotelException):
    detail = 'title не заполнен!'

class LocationNotExists(BelsHotelException):
    detail = 'location не заполнен!'


class TitleNotFoundExcetion(BelsHotelException):
    detail = 'location не заполнен!'


class HotelDeleteConstraintException(BelsHotelException):
    detail = 'Нелья удалить отель из за связанных данных!'

class HotelDublicateExeption(BelsHotelException):
    detail = 'Отель существует!'



class TitleDublicate(BelsHotelException):
    detail = 'title уже существует!'



# class FacilityNotFound(BelsHotelException):
#     def __init__(self, missing_ids):
#         self.missing_ids = missing_ids
#
#     detail = 'facilities не найдены'
#
# class FacilityNotFoundHTTPException(FacilityNotFound):
#     status_code = 409
#     detail = f'не найденые facilities: {missing_ids}'


class FacilityNotFound(BelsHotelHTTPException):
    def __init__(self, missing_ids: list[int]):
        self.missing_ids = missing_ids


# class FacilityNotFoundHTTPException(FacilityNotFound):
#     def __init__(self, missing_ids: list[int]):
#         self.missing_ids = missing_ids
#         detail = f"Не найдены facilities: {missing_ids}"
#         super().__init__(status_code=409, detail=detail)