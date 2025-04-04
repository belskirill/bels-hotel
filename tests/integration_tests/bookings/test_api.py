import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-01", "2024-08-10", 409),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-15", "2024-08-20", 2),
        (1, "2024-08-21", "2024-08-23", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, count, delete_bookings, authenticated_ac
):
    res = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert res.status_code == 200

    response = await authenticated_ac.get(
        "/bookings/me",
    )

    assert response.status_code == 200
    assert len(response.json()) == count
