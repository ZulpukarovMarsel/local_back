from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from models.base_model import Base


class Like(Base):
    __table_args__ = (
        UniqueConstraint("author_id", "post_id", name="uix_author_post"),
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
        index=True,
    )
    author: Mapped["User"] = relationship(
        "User", back_populates="likes"
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False,
        index=True,
    )
    post: Mapped["Post"] = relationship(
        "Post", back_populates="likes"
    )

    __table_args__ = (
        UniqueConstraint(
            "author_id",
            "post_id",
            name="uq_likes_author_post",
        ),
    )

    def __repr__(self):
        return f"<Like(id={self.id}, author={self.author.username}, post_id={self.post.id})>"
