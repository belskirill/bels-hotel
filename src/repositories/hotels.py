from datetime import date

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, func, insert
from sqlalchemy.exc import NoResultFound, IntegrityError

from exceptions import ObjectNotFoundException, HotelDublicateExeption
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper


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
                raise HotelDublicateExeption from ex
            else:
                raise ex

    async def get_filtered_by_time(
        self, date_from: date, date_to: date, location, title, limit, offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to
        )
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(
                    location.strip().lower()
                )
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        return [
            self.mapper.map_to_domain(hotel) for hotel in result.scalars().all()
        ]
