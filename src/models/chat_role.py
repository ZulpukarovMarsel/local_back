from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import Base


class ChatRole(Base):
    name: Mapped[str] = mapped_column()
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped["Chat"] = relationship("Chat", back_populates="chat_roles")
    participants: Mapped[List["ChatParticipant"]] = relationship("ChatParticipant", back_populates="chat_role")
    can_delete_messages: Mapped[bool] = mapped_column(default=False)
    can_add_users: Mapped[bool] = mapped_column(default=False)
    can_remove_users: Mapped[bool] = mapped_column(default=False)
    can_edit_chat: Mapped[bool] = mapped_column(default=False)
    can_change_roles: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"ChatRole(id={self.id}, name={self.name})"
