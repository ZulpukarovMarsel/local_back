import logging
from typing import List
from fastapi import APIRouter, Depends

from repositories import UserRepository
from schemas.user import (
    UserRead
)
from dependencies import get_user_repo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(lambda: None)]
)


@router.get("/users", response_model=List[UserRead], status_code=200)
async def get_users(
    user_repo: UserRepository = Depends(get_user_repo)
):
    return await user_repo.get_all()
