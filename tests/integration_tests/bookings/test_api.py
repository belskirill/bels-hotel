import pytest

@pytest.mark.parametrize('room_id, date_from, date_to, status_code', [
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-01', '2024-08-10', 200),
    (1, '2024-08-01', '2024-08-10', 500),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    db, authenticated_ac
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res



@pytest.fixture(scope="function")
async def delete_bookings(db):
    await db.bookings.delete()
    await db.commit()
    yield db


@pytest.mark.parametrize('room_id, date_from, date_to, count', [
    (1, '2024-08-01', '2024-08-10', 1),
    (1, '2024-08-15', '2024-08-20', 2),
    (1, '2024-08-21', '2024-08-23', 3),
    (1, '2024-08-25', '2024-08-27', 4),
    (1, '2024-08-28', '2024-08-29', 5),
])
async def test_add_and_get_bookings(delete_bookings, authenticated_ac, room_id, date_from, date_to, count):
    res = await authenticated_ac.post(
        '/bookings',
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    response = await authenticated_ac.get(
        "/bookings/me",
    )

    print(len(response.json()))
