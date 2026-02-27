import json
from .base_service import BaseService
from repositories import CommentRepository
from schemas.comment import CommentCreateSchema
from core.redis import redis_client
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
        await redis_client.delete(f"post:{post_id}")
        comment = await self.comment_repo.create_data(comment_data)
        cache_key = f"comment:{comment.id}"
        await redis_client.set(
            cache_key,
            json.dumps({
                "id": comment.id,
                "author_id": comment.author_id,
                "post_id": comment.post_id,
                "parent_id": comment.parent_id,
                "text": comment.text,
                "replies": []
            }),
            ex=300
        )
        return comment

    async def get_all(self, post_id: int):
        comments = await self.comment_repo.get_comments_by_post(post_id)
        result = []
        for comment in comments:
            cache_key = f"comment:{comment.id}"
            cached = await redis_client.get(cache_key)
            if cached:
                comment_data = json.loads(cached)
            else:
                comment_data = {
                    "id": comment.id,
                    "author_id": comment.author_id,
                    "post_id": comment.post_id,
                    "parent_id": comment.parent_id,
                    "text": comment.text,
                    "replies": []
                }
                await redis_client.set(cache_key, json.dumps(comment_data), ex=300)
            result.append(comment_data)
        return result
