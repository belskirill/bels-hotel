from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from exceptions import UserAlreadyExists, UserAlreadyExistsException, UserNotExists, IncorrectPassword, \
    ObjectNotFoundException
from src.config import settings
from src.schemas.users import UserRequestAdd, UserAdd
from src.service.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(
        schemes=["argon2", "bcrypt"], deprecated="auto", bcrypt__ident="2b"
    )

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен!")


    async def register_user(self, data: UserRequestAdd):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add_data(new_user_data)
            await self.db.commit()
        except UserAlreadyExists:
            raise UserAlreadyExistsException


    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotExists
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPassword
        access_token = AuthService().create_access_token({"user_id": user.id})
        return access_token


    async def get_me(self, user_id):
        try:
            user = await self.db.users.get_one(id=user_id)
            return user
        except ObjectNotFoundException:
            raise UserNotExists



