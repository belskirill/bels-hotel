from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking
from sqlalchemy import select
from datetime import date



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def add_booking(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(RoomsOrm)
            .options(selectinload(RoomsOrm.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        free_room = [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ][0]
        if not free_room:
            raise HTTPException(
                status_code=404, detail="No free rooms available for the given dates."
            )

            # Создаем новое бронирование
        new_booking = BookingsOrm(
            room_id=free_room.id,
            user_id=self.model.user_id,
            date_from=self.model.date_from,
            date_to=self.model.date_to,
            description=self.model.description,
            price=self.model.price,
        )
        session.add(new_booking)
        await session.commit()
        await session.refresh(new_booking)

        return new_booking
