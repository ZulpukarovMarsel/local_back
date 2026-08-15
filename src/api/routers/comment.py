from typing import List
from fastapi import APIRouter, Depends, HTTPException

from repositories import CommentRepository, LikeCommentRepository
from services import CommentService
from dependencies import get_comment_repo, get_like_comment_repo, get_current_user
from schemas.comment import CommentLikeStateResponseSchema

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}}
)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, comment_repo: CommentRepository = Depends(get_comment_repo)):
    return await comment_repo.delete_data(comment_id)


@router.put("/{comment_id}/like")
async def like_comment(
    comment_id: int,
    like_comment_repo: LikeCommentRepository = Depends(get_like_comment_repo),
    comment_repo: CommentRepository = Depends(get_comment_repo),
    user=Depends(get_current_user)
):
    comment = await comment_repo.get_data_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Коментарий не найден")
    like_comment = await like_comment_repo.get_like_by_comment_author_id(comment_id, user.id)
    if like_comment:
        return like_comment
    return await like_comment_repo.create_data({"comment_id": comment_id, "author_id": user.id})


@router.delete("/{comment_id}/like")
async def delete_like_comment(comment_id: int, like_comment_repo: LikeCommentRepository = Depends(get_like_comment_repo), user=Depends(get_current_user)):
    like_comment = await like_comment_repo.get_like_by_comment_author_id(comment_id, user.id)
    if not like_comment:
        raise HTTPException(status_code=404, detail="Лайк на коментарий не найден")
    return await like_comment_repo.delete_data(comment_id)
