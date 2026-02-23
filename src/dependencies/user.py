from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository, RoleRepository
from services import UserService
from dependencies.db import get_db
from dependencies.role import get_role_repo

bearer = HTTPBearer()


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repo), role_repo: RoleRepository = Depends(get_role_repo)):
    return UserService(user_repo, role_repo)
