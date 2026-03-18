from fastapi import HTTPException
from repositories import ChatRepository, ChatParticipantRepository, ChatRoleRepository, UserRepository, MessageRepository
from schemas.chat import ChatCreateSchema, ChatParticipantBase
from schemas.message import MessageBase


class ChatService:
    def __init__(self, chat_repo: ChatRepository, chat_participant_repo: ChatParticipantRepository, chat_role_repo: ChatRoleRepository, user_repo: UserRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.chat_participant_repo = chat_participant_repo
        self.chat_role_repo = chat_role_repo
        self.user_repo = user_repo
        self.message_repo = message_repo

    async def create_group_chat(self, data: ChatCreateSchema, user_id: int):
        chat = await self.chat_repo.create_data({
            "name": data.name,
            "is_group": True
        })

        chat_role = await self.chat_role_repo.create_admin({
            "name": "admin",
            "chat_id": chat.id
        })

        await self.chat_participant_repo.create_data({
            "chat_id": chat.id,
            "user_id": user_id,
            "chat_role_id": chat_role.id
        })

        participant_ids = set(data.participant_ids)
        participant_ids.discard(user_id)

        for participant_id in participant_ids:
            await self.chat_participant_repo.create_data({
                "chat_id": chat.id,
                "user_id": participant_id,
            })

        return chat

    async def create_private_chat(self, username: str, current_user_id: int, data: MessageBase):
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        chat = await self.chat_repo.get_private_chat_between_users(current_user_id, user.id)
        if not chat:
            chat = await self.chat_repo.create_data({"name": username, "is_group": False})
            role = await self.chat_role_repo.create_data({"name": "member", "chat_id": chat.id, "can_delete_messages": True, "can_add_users": False, "can_remove_users": True, "can_edit_chat": True, "can_change_roles": False})
            await self.chat_participant_repo.create_data({"chat_id": chat.id, "user_id": current_user_id, "chat_role_id": role.id})
            await self.chat_participant_repo.create_data({"chat_id": chat.id, "user_id": user.id, "chat_role_id": role.id})

        message = await self.message_repo.create_data({
            "chat_id": chat.id,
            "sender_id": current_user_id,
            "content": data.content
        })

        return {"chat_id": chat.id, "message_id": message.id}


class ChatParticipantService:
    def __init__(
            self, chat_participant_repo: ChatParticipantRepository,
            chat_repo: ChatRepository,
            user_repo: UserRepository,
            message_repo: MessageRepository
    ):
        self.chat_participant_repo = chat_participant_repo
        self.chat_repo = chat_repo
        self.user_repo = user_repo
        self.message_repo = message_repo

    async def verify_user_in_chat(self, chat_id: int, user_id: int):
        participant = await self.chat_participant_repo.get_by_user_id_and_chat_id(user_id, chat_id)
        if not participant:
            raise HTTPException(status_code=403, detail="Вы не участник этого чата")
        return participant

    async def create_chat_participant(self, data: ChatCreateSchema, user_id: int):
        return None

    async def added_participants_in_chat(
        self,
        chat_participant_data: ChatParticipantBase,
        chat_id: int,
        performer_id: int
    ):

        chat_performer = await self.verify_user_in_chat(
            chat_id,
            performer_id
        )

        if not chat_performer.chat_role.can_add_users:
            raise HTTPException(status_code=403, detail="Нет разрешения на добавление пользователей")

        performer = await self.user_repo.get_data_by_id(performer_id)
        added_users = []
        for user_id in chat_participant_data.user_ids:

            existing = await self.chat_participant_repo.get_by_user_id_and_chat_id(
                user_id,
                chat_id
            )

            if existing:
                continue

            data = {
                "user_id": user_id,
                "chat_id": chat_id
            }

            await self.chat_participant_repo.create_data(data)

            user = await self.user_repo.get_data_by_id(user_id)
            added_users.append(user.username)
        if added_users:
            users_string = ", ".join(added_users)
            await self.message_repo.create_data({
                "chat_id": chat_id,
                "sender_id": performer_id,
                "content": f"{performer.username} добавил {users_string}",
                "message_type": "system"
            })

        return {"status": "Пользователи успешно добавлены!"}

    async def delete_participants_in_chat(self, chat_id: int, performer_id: int, user_id: int):
        chat_performer = await self.verify_user_in_chat(
            chat_id,
            performer_id
        )
        if not chat_performer.chat_role.can_remove_users:
            raise HTTPException(status_code=403, detail="Нет разрешения на удаление пользователей")
        chat_participant = await self.verify_user_in_chat(
            chat_id,
            user_id
        )
        await self.chat_participant_repo.delete_data(chat_participant.id)

        performer = await self.user_repo.get_data_by_id(performer_id)
        user = await self.user_repo.get_data_by_id(user_id)

        await self.message_repo.create_data({
                "chat_id": chat_id,
                "sender_id": performer_id,
                "content": f"{performer.username} удалил {user.username}",
                "message_type": "system"
            })
        return {"status": "success", "deleted_user_id": user_id}
