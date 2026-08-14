from pydantic import Field

from schemas.common import ORMBaseSchema
from schemas.post import PostResponseSchema
from schemas.user import UserProfileResponseSchema


class SearchResponseSchema(ORMBaseSchema):
    users: list[UserProfileResponseSchema] = Field(
        default_factory=list,
    )

    posts: list[PostResponseSchema] = Field(
        default_factory=list,
    )

    next_cursor: str | None = None
    has_more: bool = False
