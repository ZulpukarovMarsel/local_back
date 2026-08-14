from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import Base


class ChatParticipant(Base):
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chat_role_id: Mapped[int] = mapped_column(
        ForeignKey("chat_roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    chat: Mapped["Chat"] = relationship("Chat", back_populates="participants")
    user: Mapped["User"] = relationship("User", back_populates="chats")
    chat_role: Mapped["ChatRole"] = relationship("ChatRole", back_populates="participants")

    __table_args__ = (
        UniqueConstraint(
            "chat_id",
            "user_id",
            name="uq_chat_participants_chat_user",
        ),
    )

    def __repr__(self):
        return f"<ChatParticipant(id={self.id}, chat_id={self.chat_id}, user_id={self.user_id})>"
