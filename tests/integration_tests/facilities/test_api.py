async def test_get_facilities(ac):
    respone = await ac.get("/facilities")

    assert respone.status_code == 200


async def test_post_add_facilities(ac):
    response = await ac.post("/facilities", json={"title": "location moscow"})

    assert response.status_code == 200
