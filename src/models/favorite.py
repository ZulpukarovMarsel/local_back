from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.base_model import Base


class Favorite(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user={self.user.username}, post_id={self.post.id})>"
