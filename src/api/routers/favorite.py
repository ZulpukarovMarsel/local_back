from fastapi import APIRouter, Depends
from typing import List
from repositories import FavoriteRepository
from dependencies import get_current_user, get_favorite_repo
from schemas.favority import FavoriteReadSchema, FavoriteCreateSchema
from core.redis import redis_client

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
    responses={404: {"description": "Not found"}}
)


@router.post("", response_model=FavoriteReadSchema)
async def create_favorite(data: FavoriteCreateSchema, favorite_repo: FavoriteRepository = Depends(get_favorite_repo), user=Depends(get_current_user)):
    favorite = await favorite_repo.create_data({
        "user_id": user.id,
        "post_id": data.post_id
    })
    await redis_client.delete(f"post:{data.post_id}")
    return FavoriteReadSchema.from_orm(favorite)


@router.get("", response_model=List[FavoriteReadSchema])
async def get_favorites(favorite_repo: FavoriteRepository = Depends(get_favorite_repo), user=Depends(get_current_user)):
    return await favorite_repo.get_all(user.id)
