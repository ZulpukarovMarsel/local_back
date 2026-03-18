from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from dependencies.db import get_db
from dependencies.user import get_user_repo
from dependencies.message import get_message_repo
from repositories import ChatRepository, ChatParticipantRepository, ChatRoleRepository, UserRepository, MessageRepository
from services import ChatService, ChatParticipantService


async def get_chat_repo(db: AsyncSession = Depends(get_db)):
    return ChatRepository(db)


async def get_chat_participant_repo(db: AsyncSession = Depends(get_db)):
    return ChatParticipantRepository(db)


async def get_chat_role_repo(db: AsyncSession = Depends(get_db)):
    return ChatRoleRepository(db)


async def get_chat_service(
        chat_repo: ChatRepository = Depends(get_chat_repo),
        chat_participant_repo: ChatParticipantRepository = Depends(get_chat_participant_repo),
        chat_role_repo: ChatRoleRepository = Depends(get_chat_role_repo),
        user_repo: UserRepository = Depends(get_user_repo),
        message_repo: MessageRepository = Depends(get_message_repo)
):
    return ChatService(chat_repo, chat_participant_repo, chat_role_repo, user_repo, message_repo)


async def get_chat_participant_service(
        chat_participant_repo: ChatParticipantRepository = Depends(get_chat_participant_repo),
        chat_repo: ChatRepository = Depends(get_chat_repo),
        user_repo: UserRepository = Depends(get_user_repo),
        message_repo: MessageRepository = Depends(get_message_repo)
):
    return ChatParticipantService(chat_participant_repo, chat_repo, user_repo, message_repo)
