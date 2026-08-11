from datetime import datetime
from typing import Generic, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from models.post import (
    MediaType,
    PostType,
    PostVisibility,
)


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )


class PostAuthorResponseSchema(ORMBaseSchema):
    id: int
    username: str
    avatar: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool = False


class PostMediaResponseSchema(ORMBaseSchema):
    id: int
    post_id: int
    media_type: MediaType
    file_url: str
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None
    duration: float | None = None
    position: int = 0


class PostMediaCreateSchema(BaseModel):
    media_type: MediaType
    file_url: str
    thumbnail_url: str | None = None

    width: int | None = Field(
        default=None,
        ge=1,
    )

    height: int | None = Field(
        default=None,
        ge=1,
    )

    duration: float | None = Field(
        default=None,
        ge=0,
    )

    position: int = Field(
        default=0,
        ge=0,
    )


class PostCreateSchema(BaseModel):
    post_type: PostType = PostType.POST

    caption: str | None = Field(
        default=None,
        max_length=2200,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    visibility: PostVisibility = PostVisibility.PUBLIC
    comments_enabled: bool = True


class PostUpdateSchema(BaseModel):
    caption: str | None = Field(
        default=None,
        max_length=2200,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    visibility: PostVisibility | None = None
    comments_enabled: bool | None = None


class PostResponseSchema(ORMBaseSchema):
    id: int
    author_id: int

    post_type: PostType
    caption: str | None = None
    location: str | None = None
    visibility: PostVisibility
    comments_enabled: bool

    author: PostAuthorResponseSchema
    media: list[PostMediaResponseSchema] = Field(
        default_factory=list,
    )

    likes_count: int = 0
    comments_count: int = 0

    liked_by_me: bool = False
    saved_by_me: bool = False

    created_at: datetime
    updated_at: datetime


class PostActionResponseSchema(BaseModel):
    success: bool = True
    message: str


class PostLikeResponseSchema(BaseModel):
    liked: bool
    likes_count: int = Field(ge=0)


class PostSaveResponseSchema(BaseModel):
    saved: bool


class PostDeleteResponseSchema(BaseModel):
    success: bool = True
    message: str = "Публикация удалена"


PaginationItem = TypeVar("PaginationItem")


class CursorPageSchema(
    BaseModel,
    Generic[PaginationItem],
):
    items: list[PaginationItem] = Field(
        default_factory=list,
    )

    next_cursor: str | None = None
    has_more: bool = False
