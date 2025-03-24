from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking
from sqlalchemy import select
from datetime import date



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper



    async def get_bookings_with_today_chekin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain(booking) for booking in res.scalars().all()]

