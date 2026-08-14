from datetime import datetime

from pydantic import BaseModel, Field

from models import StoryMediaType
from schemas.common import ORMBaseSchema
from schemas.user import UserShortResponseSchema


class StoryCreateSchema(BaseModel):
    caption: str | None = Field(
        default=None,
        max_length=500,
    )


class StoryResponseSchema(ORMBaseSchema):
    id: int
    author_id: int

    media_type: StoryMediaType
    media_url: str
    thumbnail_url: str | None = None
    caption: str | None = None

    author: UserShortResponseSchema

    views_count: int = 0
    viewed_by_me: bool = False

    created_at: datetime
    expires_at: datetime


class StoryViewResponseSchema(ORMBaseSchema):
    story_id: int
    viewed_by_me: bool = True
    views_count: int = Field(ge=0)
