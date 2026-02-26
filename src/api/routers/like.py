from fastapi import APIRouter, Depends

from repositories import LikeRepository
from dependencies import get_like_repo, get_current_user
from schemas.like import LikeCreateSchema, LikeReadSchema

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
    return LikeReadSchema.from_orm(like)
