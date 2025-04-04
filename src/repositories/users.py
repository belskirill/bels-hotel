from sqlalchemy import select
from pydantic import EmailStr

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        try:
            query = select(self.model).filter_by(email=email)
            results = await self.session.execute(query)
            model = results.scalars().one()
            return UserWithHashPassword.model_validate(model)
        except Exception as e:  # noqa
            return None
