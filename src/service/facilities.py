from src.schemas.facilities import FacilityAdd
from src.service.base import BaseService

from src.tasks.tasks import t_tasks


class FacilitiesService(BaseService):
    async def get_facilities(self):
        t_tasks.delay()
        return await self.db.facilities.get_all()


    async def create_facility(self, data: FacilityAdd):
        res = await self.db.facilities.add_data(data)
        await self.db.commit()
        t_tasks.delay()
        return res