from datetime import date

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import String

class BookingsOrm(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(foreign_key='room.id')
    user_id: Mapped[int] = mapped_column(foreign_key='user.id')
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]


    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days