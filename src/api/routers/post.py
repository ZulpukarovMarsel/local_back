from typing import List, Optional
from schemas.post import PostReadSchema
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, Security, HTTPException

from core.security import bearer
from services import PostService
from repositories import PostRepository
from dependencies import get_post_service, get_post_repo, get_current_user, get_current_user_raw

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Security(bearer)],
    # dependencies=[Depends(lambda: None)]
)


@router.get("/feed", response_model=List[PostReadSchema])
async def get_posts(request: Request, post_service: PostService = Depends(get_post_service)):
    base_url = str(request.base_url).rstrip("/")
    return await post_service.get_all(base_url=base_url)


@router.get("/{post_id}", response_model=PostReadSchema)
async def get_post(request: Request, post_id: int, post_service: PostService = Depends(get_post_service)):
    base_url = str(request.base_url).rstrip("/")
    return await post_service.get_post_by_id(post_id, base_url)


@router.post("/", response_model=PostReadSchema)
async def create_post(
    content: Optional[str] = Form(None), files: List[UploadFile] = File(default=[]),
    post_service: PostService = Depends(get_post_service), author=Depends(get_current_user_raw)
):
    return await post_service.create_post_with_attachments(author=author, content=content, files=files)


# TODO: 0.1.2 - Реализовать изменения поста
@router.patch("/{post_id}")
async def update_post(post_id: int):
    return None


# TODO: 0.1.2 - Улучшить удаение
@router.delete("/post_id")
async def delete_post(post_id: int, post_repo: PostRepository = Depends(get_post_repo)):
    post = await post_repo.get_data_by_id(post_id)
    if not post:
        return HTTPException(status_code=404, detail="Пост не найден")
    post_delete = await post_repo.delete_data(post_id)
    return "Пост удален!"


# TODO: 0.1.2 - Реализовать поставить лайк
@router.put("/{post_id}/like")
async def put_like(post_id: int):
    return None


# TODO: 0.1.2 - Реализовать убрать лайк с поста
@router.delete("/{post_id}/like")
async def delete_like(post_id: int):
    return None


# TODO: 0.1.2 - Реализовать получить всех пользавателей которые поставили лайк
@router.get("/{post_id}/likes")
async def get_likes(post_id: int):
    return None


# TODO: 0.1.3 - Реализовать получение комменты поста
# @router.get("/{post_id}/comments", response_model=List[CommentReadSchema])
# async def get_comments(post_id: int, comment_repo: CommentRepository = Depends(get_comment_repo)):
    # return await comment_repo.get_comments_by_post(post_id)

# TODO: 0.1.3 - Реализовать создание коммента для поста
# @router.post("/{post_id}/comments", response_model=CommentReadSchema)
# async def create_comment(post_id: int, data: CommentCreateSchema, comment_service: CommentService = Depends(get_comment_service), author=Depends(get_current_user)):
#     return await comment_service.create_comment(post_id, data, author)

# TODO: 0.1.4 - Реализовать сохраненние посты
# @router.put("/{post_id}/save")
# async def post_save(post_id: int):
    # return None


# TODO: 0.1.4 - Реализовать удаление сохраненноно поста
# @router.delete("{post_id}/save")
# async def delete_post_save(post_id: int):
    # return None
