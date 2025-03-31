from datetime import date
from select import select

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user,
        room_id=room,
        date_from=date(year=2024, month=8, day=20),
        date_to=date(year=2024, month=8, day=10),
        price=100,
    )
    await db.bookings.add_data(booking_data)
    await db.commit()

    res = await db.bookings.get_one_or_none(user_id=booking_data.user_id)
    assert res

    new_booking_data = BookingAdd(
        user_id=user,
        room_id=room,
        date_from=date(year=2024, month=8, day=20),
        date_to=date(year=2024, month=8, day=10),
        price=50000,
    )

    await db.bookings.edit(new_booking_data, user_id=booking_data.user_id)
    res2 = await db.bookings.get_one_or_none(user_id=new_booking_data.user_id)
    assert res2
    await db.commit()

    bookings = await db.bookings.delete(user_id=booking_data.user_id)
    assert not bookings
    await db.commit()
