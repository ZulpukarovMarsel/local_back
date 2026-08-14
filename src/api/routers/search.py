from fastapi import APIRouter, Depends, Query
from typing import List

from schemas.user import UserShortResponseSchema
from repositories import UserRepository
from dependencies import get_user_repo

router = APIRouter(
    prefix="",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search", response_model=List[UserShortResponseSchema])
async def search_users(
    q: str = Query(..., description="Username для поиска"),
    user_repo: UserRepository = Depends(get_user_repo)
):
    return await user_repo.search_by_username(q)
