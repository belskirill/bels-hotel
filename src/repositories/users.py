from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import User, UserWithHashPassword
from pydantic import EmailStr

class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper


    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        results = await self.session.execute(query)
        model = results.scalars().one()
        return UserWithHashPassword.model_validate(model)