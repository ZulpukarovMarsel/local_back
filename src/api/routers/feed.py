from fastapi import APIRouter, Depends, Request, Security

from schemas.post import CursorPageSchema, PostResponseSchema
from services import PostService
from dependencies import get_post_service, get_current_user
from core.security import bearer


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Security(bearer)],
    # dependencies=[Depends(lambda: None)]
)


@router.get("/feed", response_model=CursorPageSchema[PostResponseSchema])
async def get_feed(request: Request, post_service: PostService = Depends(get_post_service), user=Depends(get_current_user)):
    return await post_service.get_feed(username=user.username, base_url=str(request.base_url).rstrip("/"))
