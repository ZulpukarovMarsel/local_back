from sqlalchemy import select
from sqlalchemy.orm import selectinload
from repositories.base_repository import BaseRepository
from models import Post


class PostRepository(BaseRepository):
    model = Post

    async def get_all(self):
        return await super().get_all(
            selectinload(self.model.author), selectinload(self.model.attachments),
        )

    async def get_data_by_id(self, post_id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == post_id)
            .options(
                selectinload(self.model.author),
                selectinload(self.model.attachments),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
