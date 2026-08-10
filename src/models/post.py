import enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
)
from typing import List

from models.base_model import Base


# TODO: 0.1.2 - Добавить новые поля для поста: Done

class PostType(enum.Enum):
    POST = "post"
    REEL = "reel"


class PostVisibility(enum.Enum):
    PUBLIC = "public"
    FOLLOWERS = "followers"
    PRIVATE = "private"


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"


class Post(Base):
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    post_type: Mapped[PostType] = mapped_column(
        Enum(PostType),
        default=PostType.POST,
        nullable=False,
    )

    caption: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    visibility: Mapped[PostVisibility] = mapped_column(
        Enum(PostVisibility),
        default=PostVisibility.PUBLIC,
        nullable=False,
    )

    comments_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )

    media: Mapped[List["PostMedia"]] = relationship(
        "PostMedia",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="PostMedia.position",
    )

    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    likes: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Post(id={self.id}, author_id={self.author_id})>"


class PostMedia(Base):
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False,
    )

    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    thumbnail_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    duration: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="media",
    )
# TODO: 0.1.4 - Реализовать модел сохраненные посты
    # saved_posts: Mapped[List["SavedPost"]] = relationship(
    #     "SavedPost",
    #     back_populates="post",
    #     cascade="all, delete-orphan"
    # )


# TODO: 0.1.4 - Реализовать модел сохраненные посты
class SavedPost(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="saved_posts"
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False,
    )
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="saved_posts"
    )
