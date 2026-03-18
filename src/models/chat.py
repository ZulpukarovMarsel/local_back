from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import Base


class Chat(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    participants: Mapped[List["ChatParticipant"]] = relationship(
        "ChatParticipant", back_populates="chat", cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
    chat_roles: Mapped[List["ChatRole"]] = relationship(
        "ChatRole",
        back_populates="chat",
        cascade="all, delete-orphan"
    )
    is_group: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<Chat(id={self.id}, name={self.name})>"
