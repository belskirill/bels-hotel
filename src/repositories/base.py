from fastapi import HTTPException

from pygame.display import update
from sqlalchemy import select, insert, update, delete

from src.database import engine
from src.models.hotels import HotelsOrm


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        results = await self.session.execute(query)
        return results.scalars().all()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        return results.scalars().one_or_none()


    async def add_data(self, hotel_data):
        stmt_add_hotel = insert(self.model).values(**hotel_data.model_dump()).returning(self.model)
        # log = str(stmt_add_hotel.compile(engine, compile_kwargs={"literal_binds": True}))
        results = await self.session.execute(stmt_add_hotel)
        return results.scalars().one()


    async def edit(self, hotel_data, **filter_by):
        stmt_add_hotel = update(self.model).filter_by(**filter_by).values(**hotel_data.model_dump())
        await self.session.execute(stmt_add_hotel)


    async def delete(self, **filter_by):
        stmt_add_hotel = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt_add_hotel)

