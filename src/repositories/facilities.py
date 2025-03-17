from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from datetime import date

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.facilities import Facility, RoomsFacility
from src.schemas.hotels import Hotel
from sqlalchemy import select, func

class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility



class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility


