from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .base_repository import BaseRepository
from models import Favorite


class FavoriteRepository(BaseRepository):
    model = Favorite

    async def get_favorites_count(self, post_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(self.model.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_all(self, user_id: int):
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()

    async def get_favorite_by_post_user_id(self, post_id: int, user_id: int, *options) -> int:
        stmt = select(self.model).where(self.model.post_id == post_id, self.model.user_id == user_id).options(selectinload(self.model.user), selectinload(self.model.post))
        if options:
            stmt = stmt.options(*options)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
