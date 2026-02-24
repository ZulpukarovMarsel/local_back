from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from repositories import FavoriteRepository
from dependencies.db import get_db


async def get_favorite_repo(db: AsyncSession = Depends(get_db)):
    return FavoriteRepository(db)
