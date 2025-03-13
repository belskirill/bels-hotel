from pygame.display import update
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel, ConfigDict


class BaseRepository:
    model = None
    schema: BaseModel = None

    exlude_unset = True


    def __init__(self, session):
        self.session = session


    async def get_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in results.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()




    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        model = results.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def add_data(self, data):
        stmt_add_hotel = insert(self.model).values(**data.model_dump()).returning(self.model)
        # log = str(stmt_add_hotel.compile(engine, compile_kwargs={"literal_binds": True}))
        results = await self.session.execute(stmt_add_hotel)
        return results.scalars().one()


    async def edit(self, hotel_data, **filter_by):
        stmt_edit_hotel = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**hotel_data.model_dump(exclude_unset=True))
        )
        await self.session.execute(stmt_edit_hotel)


    async def delete(self, **filter_by):
        stmt_del_hotel = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt_del_hotel)

