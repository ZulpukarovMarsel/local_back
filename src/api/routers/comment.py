from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, Security
from fastapi.security import HTTPAuthorizationCredentials

# from services import
from repositories import CommentRepository
from services import CommentService
from dependencies import get_comment_repo, get_current_user, get_comment_service
from schemas.comment import CommentCreateSchema, CommentReadSchema

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}}
    # dependencies=[Depends(lambda: None)]
)

# @router.get("/", response_model=None)
# async def get_comments():


@router.post("/{post_id}", response_model=CommentReadSchema)
async def create_comment(post_id: int, data: CommentCreateSchema, comment_service: CommentService = Depends(get_comment_service), author=Depends(get_current_user)):
    return await comment_service.create_comment(post_id, data, author)


@router.get("/{post_id}", response_model=List[CommentReadSchema])
async def get_comments_by_post(post_id: int, comment_repo: CommentRepository = Depends(get_comment_repo)):
    return await comment_repo.get_comments_by_post(post_id)
