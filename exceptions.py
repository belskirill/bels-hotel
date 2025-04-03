class BelsHotelException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, args, **kwargs)


class ObjectNotFoundException(BelsHotelException):
    detail = 'Объект не найден'


class AllRoomsAreBookedException(BelsHotelException):
    detail = 'Не осталось свободных номеров'

class UserAlreadyExists(BelsHotelException):
    detail = 'Пользователь уже существует!'