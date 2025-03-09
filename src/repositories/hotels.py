from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select

from src.schemas.hotels import Hotel


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


