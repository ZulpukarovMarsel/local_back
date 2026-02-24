from typing import List, Optional
from schemas.post import PostReadSchema
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, Security
from fastapi.security import HTTPAuthorizationCredentials

from core.security import bearer
from services import PostService
from repositories import PostRepository
from dependencies import get_post_service, get_post_repo, get_current_user, get_current_user_raw
from models import Comment

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Security(bearer)],
    # dependencies=[Depends(lambda: None)]
)


@router.get("/", response_model=List[PostReadSchema])
async def get_posts(request: Request, post_service: PostService = Depends(get_post_service)):
    base_url = str(request.base_url).rstrip("/")
    # return await post_repo.get_all(selectinload(post_repo.model.author), selectinload(post_repo.model.comments).selectinload(Comment.author), selectinload(post_repo.model.attachments), selectinload(post_repo.model.likes), selectinload(post_repo.model.favorites))
    return await post_service.get_all(base_url=base_url)


@router.get("/{post_id}", response_model=PostReadSchema)
async def get_post(post_id: int, post_repo: PostRepository = Depends(get_post_repo)):
    return await post_repo.get_data_by_id(post_id)


@router.post("/", response_model=PostReadSchema)
async def create_post(
    content: Optional[str] = Form(None), files: List[UploadFile] = File(default=[]),
    post_service: PostService = Depends(get_post_service), author=Depends(get_current_user_raw)
):
    return await post_service.create_post_with_attachments(author=author, content=content, files=files)
