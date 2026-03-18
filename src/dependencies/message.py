from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from dependencies.db import get_db
from repositories import MessageRepository


async def get_message_repo(db: AsyncSession = Depends(get_db)):
    return MessageRepository(db)
