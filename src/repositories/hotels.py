from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from datetime import date

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from sqlalchemy import select

class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel



    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location.strip()}%'))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        results = await self.session.execute(query)
        return results.scalars().all()


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))


