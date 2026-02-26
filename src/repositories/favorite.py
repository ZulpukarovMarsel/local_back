from sqlalchemy import select, func

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
