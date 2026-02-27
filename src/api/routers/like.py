from fastapi import APIRouter, Depends

from repositories import LikeRepository
from dependencies import get_like_repo, get_current_user
from schemas.like import LikeCreateSchema, LikeReadSchema
from core.redis import redis_client

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}}
)


@router.post("", response_model=LikeReadSchema)
async def create_like(data: LikeCreateSchema, like_repo: LikeRepository = Depends(get_like_repo), author=Depends(get_current_user)):
    like = await like_repo.create_data({
        "author_id": author.id,
        "post_id": data.post_id
    })
    await redis_client.delete(f"post:{data.post_id}")
    return LikeReadSchema.from_orm(like)


@router.delete("/{like_id}")
async def delete_like(like_id: int, like_repo: LikeRepository = Depends(get_like_repo), author=Depends(get_current_user)):
    like = await like_repo.get_data_by_id(like_id)
    if like:
        await redis_client.delete(f"post:{like.post_id}")
        await like_repo.delete_data(like_id)
        return {"detail": "Like deleted"}
    return {"detail": "Like not found"}
