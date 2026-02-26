from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .base_repository import BaseRepository
from models import Comment


class CommentRepository(BaseRepository):
    model = Comment

    async def get_comments_count(self, post_id: int) -> int:
        stmt = select(func.count(self.model.id)).where(self.model.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_comments_by_post(
            self, post_id: int,
            limit: int = 20,
            cursor: Optional[int] = None
    ) -> List[Comment]:
        stmt = select(
            self.model
            ).where(
                self.model.post_id == post_id,
                self.model.parent_id.is_(None)
                ).order_by(
                    self.model.id.desc()
                    ).limit(
                        limit
                        ).options(
                            selectinload(self.model.author),
                            selectinload(self.model.replies).selectinload(self.model.author)
                            )
        if cursor:
            stmt = stmt.where(self.model.id < cursor)
        result = await self.db.execute(stmt)
        return result.unique().scalars().all()
