from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException
from fastapi_cache.decorator import cache
from exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, HotelNotFoundException, TitleNotExists, \
    TitleNotExistsHTTPException, LocationNotExists, TitleDublicate, LocationNotExistsHTTPException, \
    LocationhotelNotExistsHTTPException, HotelDublicateExeption, HotelDublicateHTTPExeption, \
    HotelDeleteConstraintException, HotelCloseDeleteHTTPExecption

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd, Hotel
from src.service.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
@cache(expire=30)
async def get_hotels(
    date_to: date,
    date_from: date,
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="location"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        date_to=date_to,
        date_from=date_from,
        pagination=pagination,
        location=location,
        title=title,
    )


@router.get("/{hotel_id]")
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException



@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Отель сочи", "location": "sochi_u_morya"},
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Отель дубая",
                    "location": "dubai_otel_fontan",
                },
            },
        }
    ),
):
    try:
        hotel = await HotelService(db).add_hotel(hotel_data)
    except TitleNotExists:
        raise TitleNotExistsHTTPException
    except LocationNotExists:
        raise LocationNotExistsHTTPException
    except TitleDublicate:
        raise LocationhotelNotExistsHTTPException
    except HotelDublicateExeption:
        raise HotelDublicateHTTPExeption


    return {"status": "OK", "data": hotel}


@router.patch(
    "/{hotel_id}",
    summary="update hotel data",
    description="Тут мы частично обновлеям данные об отеле: можно отправить name, а можно title",
)
async def partially_update_hotel(
    hotel_id: int, hotel_data: HotelPatch, db: DBDep
):
    try:
        await HotelService(db).path_edit_hotel(hotel_id=hotel_id, data=hotel_data)
        return {"status": "OK"}
    except TitleNotExists:
        raise TitleNotExistsHTTPException
    except LocationNotExists:
        raise LocationNotExistsHTTPException



@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).put_edit_hotel(hotel_id=hotel_id, data=hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except HotelDeleteConstraintException:
        raise HotelCloseDeleteHTTPExecption


    return {"status": "OK"}


