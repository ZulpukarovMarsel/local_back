from typing import List
from fastapi import APIRouter, Depends

from repositories import CommentRepository
from services import CommentService
from dependencies import get_comment_repo, get_current_user, get_comment_service
from schemas.comment import CommentCreateSchema, CommentReadSchema

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}}
)


# TODO: 0.1.3 - Удалить комментарий
@router.delete("{comment_id}")
async def delete_comment(comment_id: int):
    return None


# TODO: 0.1.3 - Поставить лайк комментарию
@router.put("{comment_id}/like")
async def like_comment(comment_id: int):
    return None


# TODO: 0.1.3 - Удалить лайк к  комментарию
@router.delete("{comment_id}/like")
async def delete_like_comment(comment_id: int):
    return None
