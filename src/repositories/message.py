from sqlalchemy import select
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
