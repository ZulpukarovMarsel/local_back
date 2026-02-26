from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from repositories import CommentRepository
from services import CommentService
from dependencies.db import get_db


async def get_comment_repo(db: AsyncSession = Depends(get_db)):
    return CommentRepository(db)


async def get_comment_service(comment_repo: CommentRepository = Depends(get_comment_repo)):
    return CommentService(comment_repo)
