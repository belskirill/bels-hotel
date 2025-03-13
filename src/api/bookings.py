from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsRequests, Bookings

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post('')
async def bookings(
        db: DBDep,
        data: BookingsRequests,
        user_id: UserIdDep
):
    data_price = await db.rooms.get_filtered(id=data.rooms_id)
    price = [result.price for result in data_price]

    user = await db.users.get_one_or_none(id=user_id)

    _bookings_data = Bookings(price=price[0], user_id=user.id, **data.model_dump(exclude_unset=True))
    res = await db.bookings.add_data(_bookings_data)
    await db.commit()
    return res