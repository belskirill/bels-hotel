from dataclasses import Field

from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPatch
from sqlalchemy import insert, select


router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get('')
async def get_hotels(
            pagination: PaginationDep,
            location: str | None = Query(default=None, description='location'),
            title: str | None = Query(default=None, description='Название отеля')
        ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location.strip()}%'))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%'))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        results = await session.execute(query)
        hotels = results.scalars().all()
        return hotels



@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {
        'status': 'OK'
    }


@router.post('')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples=
                  {'1': {'summary': "Sochi", "value": {
                      'title': 'Отель сочи',
                      'location': 'sochi_u_morya'
                  }}, '2': {'summary': "Dubai", "value": {
                      'title': 'Отель дубая',
                      'location': 'dubai_otel_fontan'
                  }},
                   })
                 ):
    async with async_session_maker() as session:
        stmt_add_hotel = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(stmt_add_hotel.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(stmt_add_hotel)
        await session.commit()

    return {
        'status': 'OK'
    }


# все параметры
@router.put('/{hotel_id}')
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {
        'status': 'OK'
    }


@router.get('/location')
async def get_location(
        location: str = Query(ge=1, le=30)
):
    async with async_session_maker() as session:
        query = select(HotelsOrm).filter(HotelsOrm.location.ilike(f'%{location.strip()}%'))
        res = await session.execute(query)
        hotel_loc = res.scalars().all()
        return hotel_loc


@router.patch('/{hotel_id}',
              summary='Частичное обновлние данных об отеле!',
              description='Тут мы частично обновлеям данные об отеле: можно отправить name, а можно title')
def partially_update_hotel(hotel_id: int,
                           hotel_data: HotelPatch):

    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {
        'status': 'OK'
    }
