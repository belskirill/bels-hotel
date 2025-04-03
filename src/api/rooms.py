from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import (
    RoomsAdd,
    RoomsPath,
    RoomsAddRequests,
    RoomsPathRequests,
)

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/{hotel_id}/rooms")
async def get_room(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{rooms_id}")
async def get_room_by_id(rooms_id: int, hotel_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=rooms_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int, db: DBDep, room_data: RoomsAddRequests = Body()
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add_data(_room_data)
    rooms_facilities_data = [
        RoomsFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    print(rooms_facilities_data)
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.patch(
    "/{hotel_id}/rooms/{rooms_id}",
    summary="update rooms data",
    description="Тут мы частично обновлеям данные о номере",
)
async def partially_update_room(
    db: DBDep, hotel_id: int, rooms_id: int, rooms_data: RoomsPathRequests
):
    _room_data_dict = rooms_data.model_dump(exclude_unset=True)
    _rooms_data = RoomsPath(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_rooms_data, id=rooms_id, hotel_id=hotel_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facility(
            room_id=rooms_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{rooms_id}")
async def update_room(
    db: DBDep, hotel_id: int, rooms_id: int, rooms_data: RoomsAddRequests
):
    _rooms_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    await db.rooms.edit(_rooms_data, id=rooms_id)

    await db.rooms_facilities.set_room_facility(
        room_id=rooms_id, facilities_ids=rooms_data.facilities_ids
    )
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{rooms_id}")
async def delete_room(db: DBDep, rooms_id: int, hotel_id: int):
    await db.rooms.delete(id=rooms_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}
