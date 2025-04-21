from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel

from src.database import async_session_maker
from src.service.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def check_login(request: Request):
    token = request.cookies.get("access_token", None)
    if token:
        raise HTTPException(
            status_code=409,
            detail="Вы уже авторизованы!",
        )


ChechLogin = Annotated[None, Depends(check_login)]


def check_no_login(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=409,
            detail="Вы не авторизованы!",
        )


CheckNoLogin = Annotated[None, Depends(check_no_login)]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=401, detail="Вы не предоставили токен доступа!"
        )
    return token


def current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().encode_token(token)
        return data["user_id"]
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Срок действия токена истёк",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен",
        )


UserIdDep = Annotated[int, Depends(current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
