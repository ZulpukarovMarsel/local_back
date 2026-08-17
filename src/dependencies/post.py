from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import PostRepository, CommentRepository, LikeRepository, FavoriteRepository, PostMediaRepository, UserRepository
from services import PostService
from dependencies.db import get_db
from dependencies.like import get_like_repo
from dependencies.comment import get_comment_repo
from dependencies.favorite import get_favorite_repo
from dependencies.user import get_user_repo


async def get_post_repo(db: AsyncSession = Depends(get_db)):
    return PostRepository(db)


async def get_post_media_repo(db: AsyncSession = Depends(get_db)):
    return PostMediaRepository(db)


async def get_post_service(
        post_repo: PostRepository = Depends(get_post_repo), post_media_repo: PostMediaRepository = Depends(get_post_media_repo),
        comment_repo: CommentRepository = Depends(get_comment_repo), like_repo: LikeRepository = Depends(get_like_repo), favorite_repo: FavoriteRepository = Depends(get_favorite_repo),
        user_repo: UserRepository = Depends(get_user_repo)
):
    return PostService(post_repo, post_media_repo, comment_repo, like_repo, favorite_repo, user_repo)
