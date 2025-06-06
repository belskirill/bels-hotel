from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    FacilityDataMapper,
    RoomsFacilityDataMapper,
)


class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper

    async def validate_facilities(self, data):
        stmt = select(self.model.id).where(self.model.id.in_(data))
        result = await self.session.execute(stmt)
        existing_ids = {row[0] for row in result.fetchall()}

        missing_ids = set(data) - existing_ids
        return missing_ids

    async def get_facilities(self, data):
        stmt = select(self.model).where(
            self.model.id.in_(data.facilities_ids or [])
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomsFacilityDataMapper

    async def delete(self, **filter_by):
        stmt_del_hotel = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt_del_hotel)

    async def set_room_facility(self, room_id, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)

        res = await self.session.execute(query)

        current_facilities_ids: list[int] = res.scalars().all()

        delete_facility_ids = list(
            set(current_facilities_ids) - set(facilities_ids)
        )
        insert_facility_ids = list(
            set(facilities_ids) - set(current_facilities_ids)
        )

        if delete_facility_ids:
            query = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(delete_facility_ids),
            )

            await self.session.execute(query)

        if insert_facility_ids:
            query = insert(self.model).values(  # type: ignore
                [
                    {"room_id": room_id, "facility_id": f_id}
                    for f_id in insert_facility_ids
                ]
            )

            await self.session.execute(query)

    async def delete_facilities_room(self, ids_to_delete):
        stmt = delete(self.model).where(self.model.room_id.in_(ids_to_delete))
        await self.session.execute(stmt)
