from sqlalchemy import select, func

from models import Like
from .base_repository import BaseRepository


class LikeRepository(BaseRepository):
    model = Like

    async def get_likes_count(self, post_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(self.model.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()
