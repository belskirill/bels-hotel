from fastapi import APIRouter, HTTPException, Response
from exceptions import UserAlreadyExists, UserAlreadyExistsExceptionHTTPException, UserAlreadyExistsException, \
    IncorrectPassword, UserNotExists, UserNotExistsHTTPException, IncorrectPasswordhttpException

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.service.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
     raise UserAlreadyExistsExceptionHTTPException
    return {
        "status": "OK",
    }


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    except UserNotExists:
        raise UserNotExistsHTTPException
    except IncorrectPassword:
        raise IncorrectPasswordhttpException


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        res = await AuthService(db).get_me(user_id)
        return res
    except UserNotExists:
        raise UserNotExistsHTTPException

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
