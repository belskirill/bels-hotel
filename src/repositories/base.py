from sqlalchemy import select, insert

from src.database import engine


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


    async def edit(self):
        pass