from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository, RoleRepository
from services import UserService
from dependencies.db import get_db
from dependencies.role import get_role_repo


async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repo), role_repo: RoleRepository = Depends(get_role_repo)):
    return UserService(user_repo, role_repo)
