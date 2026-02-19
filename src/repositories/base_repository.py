from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type

from models import Base


class BaseRepository:
    model: Type[Base] = None

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, *options):
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()

    async def get_data_by_id(self, id: int, *options):
        stmt = select(self.model).where(self.model.id == id)
        if options:
            stmt = stmt.options(*options)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_data(self, data: dict):
        obj = self.model(**data)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update_data(self, data_id: int, data: dict):
        obj = await self.get_data_by_id(data_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete_data(self, data_id: int):
        obj = await self.get_data_by_id(data_id)
        if not obj:
            return None
        await self.db.delete(obj)
        await self.db.flush()
        return obj
