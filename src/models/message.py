from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import Base


class Message(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sender: Mapped["User"] = relationship("User", back_populates="messages")
    content: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id}, sender_id={self.sender_id})>"
