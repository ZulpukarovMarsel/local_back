from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import RoleRepository
from dependencies.db import get_db


async def get_role_repo(db: AsyncSession = Depends(get_db)):
    return RoleRepository(db)
