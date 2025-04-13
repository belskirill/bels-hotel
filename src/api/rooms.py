from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, check_date_to_after_date_from, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException, FacilityNotFound, \
    FacilityNotFoundHTTPException

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import (
    RoomsAdd,
    RoomsPath,
    RoomsAddRequests,
    RoomsPathRequests, Rooms,
)
from src.service.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/{hotel_id}/rooms")
async def get_room(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    try:
        return await RoomsService(db).all_rooms_in_hotel(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException



@router.get("/{hotel_id}/rooms/{rooms_id}")
async def get_room_by_id(rooms_id: int, hotel_id: int, db: DBDep):
    try:
        return await RoomsService(db).get_room(rooms_id=rooms_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int, db: DBDep, room_data: RoomsAddRequests = Body()
):
    try:
        room = await RoomsService(db).create_room(
            hotel_id=hotel_id,
            room_data=room_data,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilityNotFound as ex:
        raise HTTPException(status_code=404, detail=f"Не найденные facilities: {str(ex.missing_ids)}")



    return {"status": "OK", "data": room}


@router.patch(
    "/{hotel_id}/rooms/{rooms_id}",
    summary="update rooms data",
    description="Тут мы частично обновлеям данные о номере",
)
async def partially_update_room(
    db: DBDep, hotel_id: int, rooms_id: int, rooms_data: RoomsPathRequests
):
    try:
        await RoomsService(db).partially_update_room(hotel_id, rooms_id, rooms_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{rooms_id}")
async def update_room(
    db: DBDep, hotel_id: int, rooms_id: int, rooms_data: RoomsAddRequests
):
    try:
        await RoomsService(db).put_edit_room(hotel_id=hotel_id, rooms_id=rooms_id, rooms_data=rooms_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{rooms_id}")
async def delete_room(db: DBDep, rooms_id: int, hotel_id: int):
    try:
        await RoomsService(db).delete_room(rooms_id=rooms_id, hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}
