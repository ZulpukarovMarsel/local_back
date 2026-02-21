from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import OTPRepository, UserRepository
from services import OTPService
from dependencies.db import get_db
from dependencies.user import get_user_repo


async def get_otp_repo(db: AsyncSession = Depends(get_db)):
    return OTPRepository(db)


async def get_otp_service(
    user_repo: UserRepository = Depends(get_user_repo),
    otp_repo: OTPRepository = Depends(get_otp_repo),
):
    return OTPService(user_repo, otp_repo)
