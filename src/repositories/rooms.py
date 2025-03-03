from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository


class HotelRepository(BaseRepository):
    model = RoomsOrm