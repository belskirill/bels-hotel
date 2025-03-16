from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from datetime import date

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from sqlalchemy import select, func

class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility