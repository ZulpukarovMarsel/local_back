from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from models.base_model import Base


class Like(Base):
    __table_args__ = (
        UniqueConstraint("author_id", "post_id", name="uix_author_post"),
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    author: Mapped["User"] = relationship("User", back_populates="likes")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), unique=True)
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    def __repr__(self):
        return f"<Like(id={self.id}, author={self.author.username}, post_id={self.post.id})>"
