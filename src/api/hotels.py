from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get('')
async def get_hotels(
            pagination: PaginationDep,
            db: DBDep,
            location: str | None = Query(default=None, description='location'),
            title: str | None = Query(default=None, description='Название отеля')
        ):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page or 5,
        offset=per_page * (pagination.page - 1)
    )


@router.get('/{hotel_id]')
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post('')
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples=
                  {'1': {'summary': "Sochi", "value": {
                      'title': 'Отель сочи',
                      'location': 'sochi_u_morya'
                  }}, '2': {'summary': "Dubai", "value": {
                      'title': 'Отель дубая',
                      'location': 'dubai_otel_fontan'
                  }},
                   })
                 ):
    hotel = await db.hotels.add_data(hotel_data)
    await db.commit()

    return {
        'status': 'OK',
        'data': hotel
    }


@router.patch('/{hotel_id}',
              summary='update hotel data',
              description='Тут мы частично обновлеям данные об отеле: можно отправить name, а можно title')
async def partially_update_hotel(
                        hotel_id: int,
                        hotel_data: HotelPatch,
                        db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {
        'status': 'OK'
    }


@router.put('/{hotel_id}')
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {
        'status': 'OK'
    }


@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {
        'status': 'OK'
    }
