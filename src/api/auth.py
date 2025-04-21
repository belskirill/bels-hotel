from fastapi import APIRouter, Response
from exceptions import (
    UserAlreadyExistsExceptionHTTPException,
    UserAlreadyExistsException,
    IncorrectPassword,
    UserNotExists,
    UserNotExistsHTTPException,
    IncorrectPasswordhttpException,
)

from src.api.dependencies import UserIdDep, DBDep, ChechLogin, CheckNoLogin
from src.schemas.users import UserRequestAdd
from src.service.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsExceptionHTTPException
    except IncorrectPasswordhttpException:
        raise IncorrectPasswordhttpException
    return {
        "status": "OK",
    }


@router.post("/login")
async def login_user(
    db: DBDep, data: UserRequestAdd, response: Response, chech_login: ChechLogin
):
    try:
        access_token = await AuthService(db).login_user(data)
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    except UserNotExists:
        raise UserNotExistsHTTPException
    except IncorrectPassword:
        raise IncorrectPasswordhttpException
    except IncorrectPasswordhttpException:
        raise IncorrectPasswordhttpException


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        res = await AuthService(db).get_me(user_id)
        return res
    except UserNotExists:
        raise UserNotExistsHTTPException


@router.post("/logout")
async def logout_user(response: Response, check_no_login: CheckNoLogin):
    response.delete_cookie("access_token")
    return {"status": "OK"}
