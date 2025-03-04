from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get('')
async def get_hotels(
            pagination: PaginationDep,
            location: str | None = Query(default=None, description='location'),
            title: str | None = Query(default=None, description='Название отеля')
        ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5 ,
            offset=per_page * (pagination.page - 1)
        )


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):

    async with async_session_maker() as session:
        hotel = await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {
        'status': 'OK',
        'data': hotel
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
        hotel = await HotelRepository(session).add_data(hotel_data)
        await session.commit()

    return {
        'status': 'OK',
        'data': hotel
    }


# все параметры
@router.put('/{hotel_id}')
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {
        'status': 'OK',
        'data': hotel
    }





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
