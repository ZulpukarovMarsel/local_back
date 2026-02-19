
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session


async def get_db(db: AsyncSession = Depends(get_session)):
    return db
