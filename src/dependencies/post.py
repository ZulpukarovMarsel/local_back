from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import PostRepository, AttachmentRepository, CommentRepository, LikeRepository, FavoriteRepository
from services import PostService
from dependencies.db import get_db
from dependencies.attachment import get_attachment_repo
from dependencies.like import get_like_repo
from dependencies.comment import get_comment_repo
from dependencies.favorite import get_favorite_repo


async def get_post_repo(db: AsyncSession = Depends(get_db)):
    return PostRepository(db)


async def get_post_service(
        post_repo: PostRepository = Depends(get_post_repo), attachment_repo: AttachmentRepository = Depends(get_attachment_repo),
        comment_repo: CommentRepository = Depends(get_comment_repo), like_repo: LikeRepository = Depends(get_like_repo), favorite_repo: FavoriteRepository = Depends(get_favorite_repo)
):
    return PostService(post_repo, attachment_repo, comment_repo, like_repo, favorite_repo)
