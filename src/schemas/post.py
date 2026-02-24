from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from schemas.comment import CommentReadSchema
from schemas.attachment import AttachmentReadSchema
from schemas.user import UserReadSchema


class PostBaseSchema(BaseModel):
    content: Optional[str] = None


class PostCreateSchema(PostBaseSchema):
    pass


class PostUpdateSchema(BaseModel):
    content: Optional[str] = None


class PostReadSchema(PostBaseSchema):
    id: int
    author_id: int
    author: UserReadSchema
    comments: List[CommentReadSchema] = []
    comments_count: int = 0
    likes_count: int = 0
    favorites_count: int = 0
    attachments: List["AttachmentReadSchema"] = []

    model_config = ConfigDict(from_attributes=True)


# class PostsResponse(BaseModel):
#     items: List[PostReadSchema]
