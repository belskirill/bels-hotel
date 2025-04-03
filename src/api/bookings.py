

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from exceptions import ObjectNotFoundException, AllRoomsAreBookedException

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Room not found")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.dict(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings_me(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)
