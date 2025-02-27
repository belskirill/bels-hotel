from fastapi import APIRouter, Query, Body
from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["hotels"])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'dubai', 'name': 'dubai'},
    {'id': 3, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 4, 'title': 'dubai', 'name': 'dubai'},
    {'id': 5, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 6, 'title': 'dubai', 'name': 'dubai'},
    {'id': 7, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 8, 'title': 'dubai', 'name': 'dubai'},
    {'id': 9, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 10, 'title': 'dubai', 'name': 'dubai'},
    {'id': 11, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 12, 'title': 'dubai', 'name': 'dubai'},
    {'id': 13, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 14, 'title': 'dubai', 'name': 'dubai'},
    {'id': 15, 'title': 'dubai', 'name': 'dubai'},
]


@router.get('')
def get_hotels(
            pagination: PaginationDep,
            id: int | None = Query(default=None, description='Айдишник'),
            title: str | None = Query(default=None, description='Название отеля')
        ):

    hotel_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotel_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotel_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotel_


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {
        'status': 'OK'
    }


@router.post('')
def create_hotel(
        hotel_data: Hotel = Body(openapi_examples=
                  {'1': {'summary': "Sochi", "value": {
                      'title': 'Отель сочи',
                      'name': 'sochi_u_morya'
                  }}, '2': {'summary': "Dubai", "value": {
                      'title': 'Отель дубая',
                      'name': 'dubai_otel_fontan'
                  }},
                   })
                 ):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
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
