from sqlalchemy import select
from sqlalchemy.orm import selectinload
from repositories.base_repository import BaseRepository
from models import Post, Comment


class PostRepository(BaseRepository):
    model = Post

    async def get_all(self):
        return await super().get_all(
            selectinload(self.model.author), selectinload(self.model.comments).selectinload(Comment.author), selectinload(self.model.attachments),
            selectinload(self.model.likes), selectinload(self.model.favorites)
        )

    async def get_data_by_id(self, post_id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == post_id)
            .options(
                selectinload(self.model.author),
                selectinload(self.model.attachments),
                selectinload(self.model.comments).selectinload(Comment.author),
                selectinload(self.model.likes),
                selectinload(self.model.favorites),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
