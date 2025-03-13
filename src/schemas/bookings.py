from datetime import date

from pydantic import BaseModel


class BookingsRequests(BaseModel):
    date_from: date
    date_to: date
    rooms_id: int


class Bookings(BaseModel):
    date_from: date
    date_to: date
    rooms_id: int
    price: int
    user_id: int


