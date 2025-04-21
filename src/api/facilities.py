from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.service.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_facilities()



@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAdd):
    res = await FacilitiesService(db).create_facility(facility_data)
    return res
