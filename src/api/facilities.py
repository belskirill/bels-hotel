from sys import prefix

from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get('')
async def get_facilities(
        db: DBDep
):
    return await db.facilities.get_all()


@router.post('')
async def add_facility(
        db: DBDep,
        title: str
):
    _data = FacilityAdd(title=title)
    res = await db.facilities.add_data(_data)
    db.commit()

    return res
