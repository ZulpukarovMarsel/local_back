import asyncio
import json
from core.redis import redis_client
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from services.base_service import BaseService
from repositories import (
    PostRepository, CommentRepository,
    LikeRepository, FavoriteRepository, PostMediaRepository
)
from models import User, PostType, PostVisibility, MediaType


class PostService(BaseService):
    def __init__(
            self, post_repo: PostRepository, post_media_repo: PostMediaRepository, comment_repo: CommentRepository,
            like_repo: LikeRepository, favorite_repo: FavoriteRepository
    ):
        self.post_repo = post_repo
        self.post_media_repo = post_media_repo
        self.comment_repo = comment_repo
        self.like_repo = like_repo
        self.favorite_repo = favorite_repo

    async def get_feed(self, base_url: str):
        return None

    async def create_post(self, author: User, caption: str, location: str, visibility: PostVisibility, comments_enabled: str, media: List[UploadFile]):
        if not media:
            raise HTTPException(
                status_code=400,
                detail="Добавьте изображение или видео",
            )

        if len(media) > 10:
            raise HTTPException(
                status_code=400,
                detail="Можно загрузить не более 10 файлов",
            )

        image_files: list[UploadFile] = []
        video_files: list[UploadFile] = []

        for file in media:
            content_type = file.content_type or ""

            if content_type.startswith("image/"):
                image_files.append(file)

            elif content_type.startswith("video/"):
                video_files.append(file)

            else:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Файл «{file.filename}» имеет неподдерживаемый тип. "
                        "Разрешены только изображения и видео"
                    ),
                )

        if image_files and video_files:
            raise HTTPException(
                status_code=400,
                detail="Нельзя добавлять изображения и видео в одну публикацию",
            )

        if video_files:
            if len(video_files) != 1:
                raise HTTPException(
                    status_code=400,
                    detail="Рилс должен содержать только одно видео",
                )

            post_type = PostType.REEL

        else:
            post_type = PostType.POST

        post = await self.post_repo.create_data({
            "author_id": author.id,
            "post_type": post_type,
            "caption": caption.strip() if caption else None,
            "location": location.strip() if location else None,
            "visibility": visibility,
            "comments_enabled": comments_enabled,
        })

        try:
            for position, file in enumerate(media):
                file_info = await self.upload_file(
                    file=file,
                    folder="posts",
                    allowed_types=("image/", "video/"),
                )

                uploaded_type = file_info.get(
                    "file_type",
                    file.content_type or "",
                )

                media_type = (
                    MediaType.VIDEO
                    if uploaded_type.startswith("video/")
                    else MediaType.IMAGE
                )
                print(media_type)
                await self.post_media_repo.create_data({
                    "post_id": post.id,
                    "media_type": media_type,
                    "file_url": file_info["file_path"],
                    "thumbnail_url": file_info.get("thumbnail_url"),
                    "width": file_info.get("width"),
                    "height": file_info.get("height"),
                    "duration": file_info.get("duration"),
                    "position": position,
                })

        except Exception:
            await self.post_repo.delete_data(post.id)
            raise

        created_post = await self.post_repo.get_data_by_id(post.id)

        if not created_post:
            raise HTTPException(
                status_code=500,
                detail="Не удалось получить созданную публикацию",
            )

        return created_post

    async def get_all(self, base_url: str) -> List[dict]:
        base_url = base_url.rstrip("/")
        posts = await self.post_repo.get_all()

        result: List[dict] = []
        for post in posts:
            cache_key = f"post:{post.id}"
            cached = await redis_client.get(cache_key)
            if cached:
                post_data = json.loads(cached)
            else:
                comments_count, likes_count, favorites_count = await asyncio.gather(
                    self.comment_repo.get_comments_count(post.id),
                    self.like_repo.get_likes_count(post.id),
                    self.favorite_repo.get_favorites_count(post.id),
                )

                author_avatar = getattr(post.author, "avatar", None)
                avatar_url = f"{base_url}{author_avatar}" if author_avatar else None
                post_data = {
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
                    "comments_count": comments_count,
                    "likes_count": likes_count,
                    "favorites_count": favorites_count,
                }
                await redis_client.set(
                    cache_key,
                    json.dumps(post_data),
                    ex=300
                )
            result.append(post_data)

        return result

    async def get_post_by_id(self, post_id: int, base_url: str):
        cache_key = f"post:{post_id}"
        cached = await redis_client.get(cache_key)
        if cached:
            result = json.loads(cached)
        else:
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
            await redis_client.set(
                    cache_key,
                    json.dumps(result),
                    ex=300
                )
        return result
