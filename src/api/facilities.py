from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import t_tasks

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("GO TO THE DATABASE")

    t_tasks.delay()
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAdd):
    res = await db.facilities.add_data(facility_data)
    await db.commit()

    t_tasks.delay()

    return res
