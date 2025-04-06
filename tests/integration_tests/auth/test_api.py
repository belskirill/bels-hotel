import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kirilltest@test.com", "password", 200),
        ("dd", "password", 422),
        ("@mail.ru", "password", 422),
    ],
)
async def test_register_user(email, password, status_code, ac):
    response = await ac.post(
        "auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kirilltest@test.com", "password", 200),
        ("kirilltest@test.com", "password1234", 409),
        ("test@test212121212.ru", "password", 409),
        ("test2212.ru", "password", 422),
    ],
)
async def test_login_user(email, password, status_code, ac):
    response = await ac.post(
        "auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
    if response.status_code == 200:
        assert "access_token" in response.json()
    assert ac.cookies["access_token"]


@pytest.mark.parametrize(
    "email, status_code",
    [
        ("kirilltest@test.com", 200),
    ],
)
async def test_user_me(email, status_code, ac):
    response = await ac.get(
        "auth/me",
    )

    _data_ = response.json()
    assert response.status_code == status_code
    assert _data_["email"] == email
    assert "id" in _data_
    assert "password" not in _data_
    assert "hashed_password" not in _data_


async def test_logout_user(ac):
    response = await ac.post(
        "auth/logout",
    )

    assert response.status_code == 200
    assert "access_token" not in ac.cookies
