from sqlalchemy import select, func
from .base_repository import BaseRepository
from models import Chat, ChatParticipant, ChatRole


class ChatRepository(BaseRepository):
    model = Chat

    async def get_all(self, user_id: int):
        stmt = (
            select(self.model)
            .join(ChatParticipant)
            .where(ChatParticipant.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_private_chat_between_users(self, user1_id: int, user2_id: int):
        subquery = (
            select(ChatParticipant.chat_id)
            .where(ChatParticipant.user_id.in_([user1_id, user2_id]))
            .group_by(ChatParticipant.chat_id)
            .having(func.count(ChatParticipant.user_id) == 2)
            .subquery()
        )

        query = (
            select(self.model)
            .where(
                self.model.id.in_(select(subquery.c.chat_id)),
                self.model.is_group == False
            )
        )
        result = await self.db.execute(query)
        return result.scalars().first()


class ChatParticipantRepository(BaseRepository):
    model = ChatParticipant

    async def get_by_user_id_and_chat_id(self, user_id: int, chat_id: int):
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.chat_id == chat_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


class ChatRoleRepository(BaseRepository):
    model = ChatRole

    async def create_admin(self, data: dict):
        data = {
            **data,
            "can_delete_messages": True,
            "can_add_users": True,
            "can_remove_users": True,
            "can_edit_chat": True,
            "can_change_roles": True
        }
        obj = self.model(**data)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj
