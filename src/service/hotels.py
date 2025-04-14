from plistlib import loads

from exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, TitleNotExists, \
    LocationNotExists, TitleDublicate
from src.schemas.hotels import HotelAdd, HotelPatch
from src.service.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        date_to,
        date_from,
        pagination,
        location,
        title,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1),
        )


    async def get_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        return await self.db.hotels.get_one(id=hotel_id)


    async def add_hotel(self, data: HotelAdd):
        title = data.title
        location = data.location
        if not title:
            raise TitleNotExists
        if not location:
            raise LocationNotExists

        location_check = self.get_hotel_with_check_title(title)
        if location_check:
            raise TitleDublicate
        hotel = await self.db.hotels.add_data(data)
        await self.db.commit()
        return hotel



    async def path_edit_hotel(self, hotel_id: int, data: HotelPatch):
        await self.get_hotel_with_check(hotel_id)
        if not data.title:
            raise TitleNotExists
        if not data.location:
            raise LocationNotExists
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()


    async def put_edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def get_hotel_with_check_title(self, title):
        try:
            return await self.db.hotels.get_one(title=title)
        except ObjectNotFoundException:
            return False