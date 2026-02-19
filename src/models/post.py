from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Column, Enum as SQLEnum
from enum import Enum
from typing import List

from models.base_model import Base


class PostType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class Post(Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="post")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="post")
    type: Mapped[PostType] = mapped_column(
        SQLEnum(PostType, name="post_type_enum"),
        nullable=False
    )

    def __repr__(self):
        return f"<Post(id={self.id})>"
