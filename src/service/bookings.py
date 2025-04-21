from exceptions import AllRoomsAreBookedException
from src.api.dependencies import UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.service.base import BaseService
from src.service.hotels import HotelService
from src.service.rooms import RoomsService


class BookingsService(BaseService):
    async def add_booking(self, booking_data: BookingAddRequest, user_id: UserIdDep):

        room = await RoomsService(self.db).get_with_check_rooms(rooms_id=booking_data.room_id)
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=room.hotel_id)

        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.dict(),
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
            await self.db.commit()
            return booking
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException




    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_bookings_me(self, user_id):
        return await self.db.bookings.get_filtered(user_id=user_id)