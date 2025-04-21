from pydantic import BaseModel

from exceptions import FacilityNotFound
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

    async def validate_facilirt(self, data: BaseModel):
        missing_ids = await self.db.facilities.validate_facilities(
            data.facilities_ids
        )
        if missing_ids:
            raise FacilityNotFound(missing_ids)

            # raise HTTPException(
            #     status_code=400,
            #     detail=f"Следующие facilities_id не найдены: {missing_ids}"
            # )
