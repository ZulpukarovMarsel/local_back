from sqlalchemy import select, union, literal, or_, and_
from sqlalchemy.orm import selectinload
from repositories.base_repository import BaseRepository
from models import Post, PostMedia, PostType, UserFollow, PostVisibility


class PostRepository(BaseRepository):
    model = Post

    async def get_by_username_and_type(self, username: str, content_type: PostType):
        stmt = (
            select(self.model)
            .where(self.model.author.has(username=username), self.model.post_type == content_type)
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

    async def get_feed(
        self,
        current_user_id: int,
        limit: int = 20,
        offset: int = 0,
    ):
        following_ids = (
            select(UserFollow.following_id.label("user_id"))
            .where(UserFollow.follower_id == current_user_id)
        )

        follower_ids = (
            select(UserFollow.follower_id.label("user_id"))
            .where(UserFollow.following_id == current_user_id)
        )

        feed_author_ids = union(
            following_ids,
            follower_ids,
            select(literal(current_user_id).label("user_id")),
        ).subquery()

        stmt = (
            select(Post)
            .where(
                Post.author_id.in_(
                    select(feed_author_ids.c.user_id)
                ),
                Post.post_type == PostType.POST,
                or_(
                    Post.author_id == current_user_id,

                    Post.visibility == PostVisibility.PUBLIC,

                    and_(
                        Post.visibility == PostVisibility.FOLLOWERS,
                        Post.author_id.in_(following_ids),
                    ),
                ),
            )
            .options(
                selectinload(Post.author),
                selectinload(Post.media),
            )
            .order_by(
                Post.created_at.desc(),
                Post.id.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().unique().all()


class PostMediaRepository(BaseRepository):
    model = PostMedia
