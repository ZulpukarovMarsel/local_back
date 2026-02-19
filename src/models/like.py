from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.base_model import Base


class Like(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    def __repr__(self):
        return f"<Like(id={self.id}, user={self.user.username}, post_id={self.post.id})>"
