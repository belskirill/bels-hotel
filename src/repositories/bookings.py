from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Rooms
