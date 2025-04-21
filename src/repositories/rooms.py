from datetime import date

from asyncpg import ForeignKeyViolationError
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound, IntegrityError

from exceptions import RoomNotFoundException, RoomDeleteConstraintException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def delete_room_in_hotel(self, ids_to_delete):
        stmt = delete(self.model).where(self.model.id.in_(ids_to_delete))
        await self.session.execute(stmt)

    async def delete(self, **filter_by):
        try:
            stmt_del_hotel = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt_del_hotel)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise RoomDeleteConstraintException from ex
            else:
                raise ex

    async def get_filtered_by_time(
        self, hotel_id, date_from: date, date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)

        return [
            RoomWithRels.model_validate(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        results = await self.session.execute(query)

        try:
            model = results.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomWithRels.model_validate(model, from_attributes=True)
