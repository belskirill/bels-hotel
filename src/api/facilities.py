

from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd, Facility

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get('')
async def get_facilities(
        db: DBDep
):
    return await db.facilities.get_all()


@router.post('')
async def add_facility(
        db: DBDep,
        facility_data: FacilityAdd
):
    res = await db.facilities.add_data(facility_data)
    await db.commit()

    return res
