from datetime import datetime

from pydantic import Field

from schemas.common import ORMBaseSchema


class UserShortResponseSchema(ORMBaseSchema):
    id: int
    username: str
    avatar: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserProfileResponseSchema(UserShortResponseSchema):
    bio: str | None = None

    posts_count: int = 0
    followers_count: int = 0
    following_count: int = 0

    followed_by_me: bool = False

    created_at: datetime | None = None
    updated_at: datetime | None = None


class FollowStateResponseSchema(ORMBaseSchema):
    user_id: int
    followed_by_me: bool
    followers_count: int = Field(ge=0)


class UserFollowResponseSchema(ORMBaseSchema):
    id: int
    follower_id: int
    following_id: int

    follower: UserShortResponseSchema
    following: UserShortResponseSchema

    created_at: datetime
