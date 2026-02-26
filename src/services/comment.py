from .base_service import BaseService
from repositories import CommentRepository
from schemas.comment import CommentCreateSchema
from models import User


class CommentService(BaseService):
    def __init__(self, comment_repo: CommentRepository):
        self.comment_repo = comment_repo

    async def create_comment(self, post_id: int, data: CommentCreateSchema, author: User):
        comment_data = {
            "author_id": author.id,
            "post_id": post_id,
            "parent_id": data.parent_id if data.parent_id else None,
            "text": data.text
        }
        return await self.comment_repo.create_data(comment_data)
