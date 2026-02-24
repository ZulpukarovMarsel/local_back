from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from repositories import CommentRepository
from dependencies.db import get_db


async def get_comment_repo(db: AsyncSession = Depends(get_db)):
    return CommentRepository(db)
