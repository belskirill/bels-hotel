from typing import Sequence, Optional
from sqlalchemy import select, insert, delete, update
from sqlalchemy.sql.sqltypes import SchemaType

from exceptions import ObjectNotFoundException, UserAlreadyExists
from sqlalchemy.exc import NoResultFound, IntegrityError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from pydantic import BaseModel

from src.database import Base
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*filter)
        results = await self.session.execute(query)
        return [
            self.mapper.map_to_domain(model)
            for model in results.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> Optional[SchemaType]:
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        model = results.scalars().one_or_none()
        if not model:
            return None
        return self.mapper.map_to_domain(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        results = await self.session.execute(query)
        try:
            model = results.scalar_one()
            return self.mapper.map_to_domain(model)
        except NoResultFound:
            raise ObjectNotFoundException

    async def add_data(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain(model)
        except NoResultFound:
            raise ObjectNotFoundException
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise UserAlreadyExists from ex
            else:
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values(
            [item.model_dump() for item in data]
        )

        await self.session.execute(add_data_stmt)

    async def edit(self, hotel_data, **filter_by) -> None:
        stmt_edit_hotel = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**hotel_data.model_dump(exclude_unset=True))
        )
        await self.session.execute(stmt_edit_hotel)

    async def delete(self, **filter_by):
        try:
            stmt_del_hotel = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt_del_hotel)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from ex
            else:
                raise ex
