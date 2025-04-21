from fastapi import APIRouter
from exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
)

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest
from src.service.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingsService(db).add_booking(
            user_id=user_id, booking_data=booking_data
        )
        return {"status": "OK", "data": booking}
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get("/me")
async def get_bookings_me(user_id: UserIdDep, db: DBDep):
    return await BookingsService(db).get_bookings_me(user_id)
