from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from models.base_model import Base
from models.association_tables import user_role


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, nullable=False, default=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True, default="")
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    roles: Mapped[List["Role"]] = relationship(secondary=user_role, back_populates="users", lazy="selectin")
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="author")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="user")
    like_comments: Mapped[List["LikeComment"]] = relationship(
        "LikeComment",
        back_populates="author"
    )

    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
