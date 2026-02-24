from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import List

from models.base_model import Base


class Post(Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="post")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="post")
    content: Mapped[str] = mapped_column(nullable=True)
    attachments: Mapped[List["Attachment"]] = relationship(
        "Attachment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post(id={self.id})>"
