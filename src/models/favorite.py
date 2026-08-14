from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from models.base_model import Base


class Favorite(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    post: Mapped["Post"] = relationship("Post", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_favorites_user_post",
        ),
    )

    def __repr__(self):
        return f"<Favorite(id={self.id}, user={self.user.username}, post_id={self.post.id})>"
