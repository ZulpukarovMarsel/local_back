from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Text, UniqueConstraint
from typing import Optional, List

from models.base_model import Base


class Comment(Base):
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="comments")

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    text: Mapped[str] = mapped_column(Text, nullable=False)
    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="replies",
        lazy="selectin"
    )

    replies: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    like_comments: Mapped[List["LikeComment"]] = relationship(
        "LikeComment",
        back_populates="comment"
    )

    def __repr__(self):
        return f"<Comment(id={self.id})>"


class LikeComment(Base):
    __table_args__ = (
        UniqueConstraint("author_id", "comment_id", name="uix_author_comment"),
    )
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    comment: Mapped["Comment"] = relationship("Comment", back_populates="like_comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="like_comments")

    def __repr__(self):
        return f"<Like comment(id={self.id}, author={self.author.username}, post={self.id})>"
