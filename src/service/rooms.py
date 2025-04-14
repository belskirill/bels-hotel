from exceptions import check_date_to_after_date_from, ObjectNotFoundException, \
    RoomNotFoundException, RoomDeleteConstraintException
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomsAddRequests, RoomsAdd, RoomsPathRequests, RoomsPath
from src.service.base import BaseService
from src.service.facilities import FacilitiesService
from src.service.hotels import HotelService


class RoomsService(BaseService):
    async def all_rooms_in_hotel(
        self,
        date_from,
        date_to,
        hotel_id
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, rooms_id, hotel_id):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_with_check_rooms(rooms_id)
        return await self.db.rooms.get_one_with_rels(id=rooms_id, hotel_id=hotel_id)

    async def create_room(
        self,
        hotel_id,
        room_data: RoomsAddRequests,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await FacilitiesService(self.db).validate_facilirt(room_data)
        _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add_data(_room_data)
        rooms_facilities_data = [
            RoomsFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        if rooms_facilities_data:
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
            await self.db.commit()


        facilities = await self.db.facilities.get_facilities(room_data)


        room_dict = room.model_dump()
        room_dict["facilities"] = [{"id": f.id, "title": f.title} for f in facilities]

        return room_dict


    async def partially_update_room(
        self, hotel_id: int, rooms_id: int, rooms_data: RoomsPathRequests
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_with_check_rooms(rooms_id)
        _room_data_dict = rooms_data.model_dump(exclude_unset=True)
        _rooms_data = RoomsPath(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_rooms_data, id=rooms_id, hotel_id=hotel_id)

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facility(
                room_id=rooms_id, facilities_ids=_room_data_dict["facilities_ids"]
            )

        await self.db.commit()

    async def put_edit_room(
        self,
        hotel_id: int,
        rooms_id: int,
        rooms_data: RoomsAddRequests,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_with_check_rooms(rooms_id)
        _rooms_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
        await self.db.rooms.edit(_rooms_data, id=rooms_id)

        await self.db.rooms_facilities.set_room_facility(
            room_id=rooms_id, facilities_ids=rooms_data.facilities_ids
        )
        await self.db.commit()

    async def delete_room(self, hotel_id, rooms_id):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_with_check_rooms(rooms_id)
        await self.db.rooms_facilities.delete(room_id=rooms_id)
        await self.db.commit()
        try:
            await self.db.rooms.delete(id=rooms_id)
            await self.db.commit()
        except RoomDeleteConstraintException:
            raise RoomDeleteConstraintException


    async def get_with_check_rooms(self, rooms_id):
        try:
            return await self.db.rooms.get_one(id=rooms_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
