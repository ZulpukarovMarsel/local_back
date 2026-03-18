from fastapi import HTTPException
from repositories import MessageRepository, ChatParticipantRepository


class MessageService:
    def __init__(self, message_repo: MessageRepository, chat_participant_repo: ChatParticipantRepository):
        self.message_repo = message_repo
        self.chat_participant_repo = chat_participant_repo

    async def get_all(self, chat_id: int, user_id: int):
        is_user_in_chat = await self.chat_participant_repo.get_by_user_id_and_chat_id(user_id, chat_id)
        if not is_user_in_chat:
            raise HTTPException(status_code=403, detail="Вы не участник этого чата") 
        return await self.message_repo.get_all_by_chat_id(chat_id)
    # async def create_message(self, chat_id: int, sender_id: int, content: str):

    #     return None
