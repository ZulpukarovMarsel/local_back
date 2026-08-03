from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from .base_repository import BaseRepository
from models import Message


class MessageRepository(BaseRepository):
    model = Message

    async def get_all_by_chat_id(self, chat_id: int):
        stmt = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .options(
                selectinload(self.model.sender),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_messages_by_chat_id(self, chat_id: int, limit: int = 20, offset: int = 0):
        stmt = (
            select(self.model)
            .where(self.model.chat_id == chat_id)
            .options(selectinload(self.model.sender))
            .order_by(desc(self.model.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
