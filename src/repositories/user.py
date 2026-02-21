from typing import List, Any
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic.networks import EmailStr

from models import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = User

    async def get_data_by_id(self, id: int, *options):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(User.roles))
        )
        if options:
            stmt = stmt.options(*options)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids(self, user_ids: list[int]):
        if not user_ids:
            return []
        result = await self.db.execute(
            select(self.model)
            .where(self.model.id.in_(user_ids))
            .options(selectinload(User.roles))
        )
        return list(result.unique().scalars().all())

    async def get_by_email(self, email: EmailStr):
        result = await self.db.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()

    async def get_by_email_and_username(self, email: EmailStr, username: str):
        result = await self.db.execute(select(self.model).where(self.model.email == email, self.model.username == username))
        return result.scalar_one_or_none()

    async def get_by_id_with_roles(self, user_id: int):
        stmt = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
