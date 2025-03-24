from pathlib import Path

from src.service.auth import AuthService
import sys



def test_create_access_token():
    data = {'user_id': 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)



