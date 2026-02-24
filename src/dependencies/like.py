from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from repositories import LikeRepository
from dependencies.db import get_db


async def get_like_repo(db: AsyncSession = Depends(get_db)):
    return LikeRepository(db)
