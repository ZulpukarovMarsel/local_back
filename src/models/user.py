from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, ForeignKey, UniqueConstraint,
    CheckConstraint, Index
)
from typing import List

from models.base_model import Base
from models.association_tables import user_role


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True, default="")
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    bio: Mapped[str | None] = mapped_column(String(150), nullable=True)
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
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="sender")
    chats: Mapped[List["ChatParticipant"]] = relationship("ChatParticipant", back_populates="user", cascade="all, delete-orphan")

    followers: Mapped[List["UserFollow"]] = relationship("UserFollow", foreign_keys="UserFollow.following_id", back_populates="following", cascade="all, delete-orphan")
    followings: Mapped[List["UserFollow"]] = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower", cascade="all, delete-orphan")
# TODO: 0.1.4 - Реализовать модел сохраненные посты
    # saved_posts: Mapped[List["SavedPost"]] = relationship(
    #         "SavedPost",
    #         back_populates="user",
    #         cascade="all, delete-orphan"
    #     )

    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class UserFollow(Base):
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="followings")

    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    following: Mapped["User"] = relationship("User", foreign_keys=[following_id], back_populates="followers")

    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="uq_user_follows_follower_following",
        ),
        CheckConstraint(
            "follower_id != following_id",
            name="ck_user_follows_no_self_follow",
        ),
        Index(
            "ix_user_follows_follower_created_at",
            "follower_id",
            "created_at",
        ),
        Index(
            "ix_user_follows_following_created_at",
            "following_id",
            "created_at",
        ),
    )
