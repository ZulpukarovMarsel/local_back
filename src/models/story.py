import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    Enum,
    String
)

from base_model import Base

# TODO: 0.1.5 - Реализовать модел сторис

# class StoryMediaType(Enum):
#     IMAGE = "image"
#     VIDEO = "VIDEO"


# class Story(Base):
#     author_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         nullable=True
#     )
#     author: Mapped["User"] = relationship(
#         "User",
#         back_populates="stories"
#     )
#     media_type: Mapped[StoryMediaType] = mapped_column(
#         Enum(StoryMediaType),
#         nullable=False
#     )
#     media_url: Mapped[str] = mapped_column(
#         String(500),
#         nullable=False
#     )
#     thumbnail_url: Mapped[str | None] = mapped_column(
#             String(500),
#             nullable=True,
#     )
#     caption: Mapped[str | None] = mapped_column(
#         nullable=True
#     )
#     expires_at:
#     deleted_at:


# class StoryView(Base):
#     story_id: Mapped[int] = mapped_column(
#         ForeignKey("stories.id"),
#         nullable=False
#     )
#     story: Mapped["Story"] = relationship(
#         "Story",
#         back_populates="story_views"
#     )
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         nullable=False
#     )
#     user: Mapped["User"] = relationship(
#         "User",
#         back_populates="story_views"
#   )
#   view_at: create_at
