from email.policy import default

from fastapi import APIRouter, Body, Query
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsPath

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get('')
async def get_room(
            hotel_id: int | None = Query(default=None, description='hotel_id'),
            title: str | None = Query(default=None, description='Название номера'),
            description: str | None = Query(default=None, description='Описание'),
            price: int | None = Query(default=None, description='price'),
            quantity: int | None = Query(default=None, description='quantity')
        ):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description,
            price=price,
            quantity=quantity
        )




@router.get('/{rooms_id]')
async def get_room_by_id(rooms_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=rooms_id)


@router.post('')
async def create_room(
        rooms_data: RoomsAdd = Body(openapi_examples=
                  {'1': {'summary': '1', "value": {
                      'hotel_id': 3,
                      'title': 'luxary',
                      'description': 'all unclusive',
                      'price': 100000,
                      'quantity': 1
                  }}
                   })
                 ):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).add_data(rooms_data)
        await session.commit()

    return {
        'status': 'OK',
        'data': rooms
    }


@router.patch('/{rooms_id}',
              summary='update rooms data',
              description='Тут мы частично обновлеям данные о номере')
async def partially_update_room(rooms_id: int,
                           rooms_data: RoomsPath):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_data, id=rooms_id)
        await session.commit()

    return {
        'status': 'OK'
    }


@router.put('/{rooms_id}')
async def update_room(rooms_id: int, rooms_data: RoomsAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_data, id=rooms_id)
        await session.commit()

    return {
        'status': 'OK'
    }


@router.delete('/{rooms_id}')
async def delete_room(rooms_id: int):

    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=rooms_id)
        await session.commit()
    return {
        'status': 'OK'
    }
