from datetime import date

from exceptions import AllRoomsAreBookedException
from sqlalchemy import select, delete

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_chekin(self):
        query = select(BookingsOrm).filter(
            BookingsOrm.date_from == date.today()
        )
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain(booking)
            for booking in res.scalars().all()
        ]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add_data(data)
            return new_booking
        raise AllRoomsAreBookedException

    async def delete_bookings(self, ids_to_delete):
        stmt = delete(self.model).where(self.model.room_id.in_(ids_to_delete))
        await self.session.execute(stmt)
