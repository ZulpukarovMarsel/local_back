import asyncio

from typing import Optional, List
from fastapi import UploadFile
from services.base_service import BaseService
from repositories import (
    PostRepository, AttachmentRepository, CommentRepository,
    LikeRepository, FavoriteRepository
)
from models import User


class PostService(BaseService):
    def __init__(
            self, post_repo: PostRepository, attachment_repo: AttachmentRepository,
            comment_repo: CommentRepository, like_repo: LikeRepository, favorite_repo: FavoriteRepository
    ):
        self.post_repo = post_repo
        self.attachment_repo = attachment_repo
        self.comment_repo = comment_repo
        self.like_repo = like_repo
        self.favorite_repo = favorite_repo

    async def create_post_with_attachments(self, author: User, content: Optional[str], files: List[UploadFile]):
        post = await self.post_repo.create_data({"author_id": author.id, "content": content})

        for f in files:
            file_info = await self.upload_file(
                file=f,
                folder="posts",
                allowed_types=("image/", "video/"),
            )

            file_type = (
                "video"
                if file_info["file_type"].startswith("video/")
                else "image"
            )

            await self.attachment_repo.create_data({
                "post_id": post.id,
                "file_path": file_info["file_path"],
                "file_type": file_type,
            })

        return await self.post_repo.get_data_by_id(post.id)

    async def get_all(self, base_url: str) -> List[dict]:
        base_url = base_url.rstrip("/")
        posts = await self.post_repo.get_all()

        result: List[dict] = []
        for post in posts:
            comments_count, likes_count, favorites_count = await asyncio.gather(
                self.comment_repo.get_comments_count(post.id),
                self.like_repo.get_likes_count(post.id),
                self.favorite_repo.get_favorites_count(post.id),
            )

            author_avatar = getattr(post.author, "avatar", None)
            avatar_url = f"{base_url}{author_avatar}" if author_avatar else None

            result.append({
                "id": post.id,
                "content": post.content,
                "author_id": post.author_id,
                "author": {
                    "id": post.author.id,
                    "username": post.author.username,
                    "email": post.author.email,
                    "first_name": post.author.first_name,
                    "last_name": post.author.last_name,
                    "roles": post.author.roles,
                    "avatar": avatar_url,
                },
                "attachments": [
                    {
                        "id": a.id,
                        "post_id": a.post_id,
                        "file_path": f"{base_url}{a.file_path}",
                        "file_type": a.file_type,
                    } for a in post.attachments
                ],
                "comments": [
                    {
                        "id": c.id,
                        "author_id": c.author_id,
                        "post_id": c.post_id,
                        "parent_id": c.parent_id,
                        "text": c.text,
                    } for c in post.comments
                ],
                "comments_count": comments_count,
                "likes_count": likes_count,
                "favorites_count": favorites_count,
            })

        return result

    async def get_post_by_id(self, post_id: int, base_url: str):
        base_url = base_url.rstrip("/")
        post = await self.post_repo.get_data_by_id(post_id)

        comments_count, likes_count, favorites_count = await asyncio.gather(
            self.comment_repo.get_comments_count(post.id),
            self.like_repo.get_likes_count(post.id),
            self.favorite_repo.get_favorites_count(post.id),
        )

        author_avatar = getattr(post.author, "avatar", None)
        avatar_url = f"{base_url}{author_avatar}" if author_avatar else None

        result = {
            "id": post.id,
            "content": post.content,
            "author_id": post.author_id,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
                "email": post.author.email,
                "first_name": post.author.first_name,
                "last_name": post.author.last_name,
                "roles": post.author.roles,
                "avatar": avatar_url,
            },
            "attachments": [
                {
                    "id": a.id,
                    "post_id": a.post_id,
                    "file_path": f"{base_url}{a.file_path}",
                    "file_type": a.file_type,
                } for a in post.attachments
            ],
            "comments": [
                {
                    "id": c.id,
                    "author_id": c.author_id,
                    "post_id": c.post_id,
                    "parent_id": c.parent_id,
                    "text": c.text,
                } for c in post.comments
            ],
            "comments_count": comments_count,
            "likes_count": likes_count,
            "favorites_count": favorites_count,
        }
        return result
