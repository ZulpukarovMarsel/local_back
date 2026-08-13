from sqlalchemy import select
from sqlalchemy.orm import selectinload
from repositories.base_repository import BaseRepository
from models import Post, PostMedia


class PostRepository(BaseRepository):
    model = Post

    # async def get_all(self):
    #     return await super().get_all(
    #         selectinload(self.model.author),
    #     )
    async def get_posts_by_username(self, username: str):
        stmt = (
            select(self.model)
            .where(self.model.author.has(username=username), self.model.post_type == "post")
            .options(
                selectinload(self.model.author),
                selectinload(self.model.media),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_reels_by_username(self, username: str):
        stmt = (
            select(self.model)
            .where(self.model.author.has(username=username), self.model.post_type == "reel")
            .options(
                selectinload(self.model.author),
                selectinload(self.model.media),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_data_by_id(self, post_id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == post_id)
            .options(
                selectinload(self.model.author),
                selectinload(self.model.media),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_data_by_username(self, username: str):
        stmt = (
            select(self.model)
            .where(self.author.username == username)
            .options(
                selectinload(self.model.author),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()


class PostMediaRepository(BaseRepository):
    model = PostMedia
