from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from models import Like
from .base_repository import BaseRepository


class LikeRepository(BaseRepository):
    model = Like

    async def get_likes_count(self, post_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(self.model.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_like_by_post_id(self, post_id: int, author_id: int, *options) -> int:
        stmt = select(self.model).where(self.model.id == id).where(self.post.id == post_id).options(selectinload(self.model.author), selectinload(self.model.post))

        if options:
            stmt = stmt.options(*options)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
