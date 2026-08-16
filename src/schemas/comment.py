from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field

from schemas.common import ORMBaseSchema
from schemas.user import UserShortResponseSchema


class CommentCreateSchema(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
    )

    parent_id: int | None = None


class CommentUpdateSchema(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
    )


class CommentResponseSchema(ORMBaseSchema):
    id: int
    post_id: int
    author_id: int
    parent_id: int | None = None

    text: str = Field(
        validation_alias=AliasChoices("content", "text"),
    )

    author: UserShortResponseSchema

    likes_count: int = 0
    liked_by_me: bool = False

    replies: list["CommentResponseSchema"] = Field(
        default_factory=list,
    )

    created_at: datetime
    updated_at: datetime


class CommentLikeStateResponseSchema(ORMBaseSchema):
    comment_id: int
    liked_by_me: bool
    likes_count: int = Field(ge=0)
