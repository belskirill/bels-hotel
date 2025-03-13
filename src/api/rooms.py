from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsAdd, RoomsPath, RoomsAddRequests, RoomsPathRequests

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get('/{hotel_id}/rooms')
async def get_room(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{rooms_id}')
async def get_room_by_id(rooms_id: int, hotel_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=rooms_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/room')
async def create_room(
        db: DBDep,
        hotel_id: int,
        rooms_data: RoomsAddRequests = Body(openapi_examples=
                  {'1': {'summary': '1', "value": {
                      'title': 'luxary',
                      'description': 'all unclusive',
                      'price': 100000,
                      'quantity': 1
                  }}
                   })
                 ):
    _rooms_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    rooms = await db.rooms.add_data(_rooms_data)
    await db.commit()

    return {
        'status': 'OK',
        'data': rooms
    }


@router.patch('/{hotel_id}/rooms/{rooms_id}',
              summary='update rooms data',
              description='Тут мы частично обновлеям данные о номере')
async def partially_update_room(
                db: DBDep,
                hotel_id: int,
                rooms_id: int,
                rooms_data: RoomsPathRequests):
    _rooms_data = RoomsPath(hotel_id=hotel_id, **rooms_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_rooms_data, id=rooms_id, hotel_id=hotel_id)
    await db.commit()

    return {
        'status': 'OK'
    }


@router.put('/{hotel_id}/rooms/{rooms_id}')
async def update_room(db: DBDep, hotel_id: int, rooms_id: int, rooms_data: RoomsAddRequests):
    _rooms_data = RoomsAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    await db.rooms.edit(_rooms_data, id=rooms_id)
    await db.commit()

    return {
        'status': 'OK'
    }


@router.delete('/{hotel_id}/rooms/{rooms_id}')
async def delete_room(db: DBDep, rooms_id: int, hotel_id: int):
    await db.rooms.delete(id=rooms_id, hotel_id=hotel_id)
    await db.commit()

    return {
        'status': 'OK'
    }
