from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms
from sqlalchemy import select


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms


    # async def get_all(
    #         self,
    #         hotel_id,
    #         title,
    #         description,
    #         price,
    #         quantity,
    # ):
    #     query = select(RoomsOrm)
    #     if hotel_id:
    #         query = query.filter(RoomsOrm.hotel_id == hotel_id)
    #     if title:
    #         query = query.filter(RoomsOrm.title.ilike(f'%{title}%'))
    #     if description:
    #         query = query.filter(RoomsOrm.description.ilike(f'%{description}%'))
    #     if price:
    #         query = query.filter(RoomsOrm.price == price)
    #     if quantity:
    #         query = query.filter(RoomsOrm.quantity == quantity)
    #     results = await self.session.execute(query)
    #     return results.scalars().all()