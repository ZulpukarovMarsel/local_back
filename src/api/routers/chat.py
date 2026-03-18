from fastapi import APIRouter, Depends
from repositories import ChatRepository, ChatParticipantRepository, MessageRepository
from dependencies import (
    get_current_user, get_chat_repo,
    get_chat_participant_repo, get_chat_service, get_message_repo,
    get_chat_participant_service
)
from schemas.chat import ChatCreateSchema, ChatParticipantBase
from schemas.message import MessageBase
from services import ChatService, ChatParticipantService
# from core.redis import redis_client

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}}
)


@router.get("")
async def get_chats(chat_repo: ChatRepository = Depends(get_chat_repo), user=Depends(get_current_user)):
    return await chat_repo.get_all(user.id)


@router.post("")
async def create_groups(data: ChatCreateSchema, chat_service: ChatService = Depends(get_chat_service),
                        user=Depends(get_current_user)):
    return await chat_service.create_group_chat(data, user.id)


@router.get("/{chat_id}")
async def get_chat(chat_id: int, chat_repo: ChatRepository = Depends(get_chat_repo), user=Depends(get_current_user)):
    return await chat_repo.get_data_by_id(chat_id)


@router.delete("/{chat_id}")
async def delete_chat(chat_id: int, chat_repo: ChatParticipantRepository = Depends(get_chat_participant_repo), user=Depends(get_current_user)):
    return await chat_repo.delete_data(chat_id)


@router.get("/{chat_id}/messages")
async def get_messages_chat(chat_id: int, message_repo: MessageRepository = Depends(get_message_repo)):
    return await message_repo.get_all_by_chat_id(chat_id)


@router.post("/{chat_id}/messages")
async def create_message_chat(chat_id: int, data: MessageBase, message_repo: MessageRepository = Depends(get_message_repo), user=Depends(get_current_user)):
    return await message_repo.create_data({"chat_id": chat_id, "sender_id": user.id, "content": data.content})


@router.delete("/{chat_id}/messages/{message_id}")
async def delete_message_chat(chat_id: int, message_id: int, message_repo: MessageRepository = Depends(get_message_repo)):
    return await message_repo.delete_data(message_id)


@router.post("/{chat_id}/participants")
async def added_participants_in_chat(chat_id: int, data: ChatParticipantBase, participant_service: ChatParticipantService = Depends(get_chat_participant_service), user=Depends(get_current_user)):
    return await participant_service.added_participants_in_chat(data, chat_id, user.id)


@router.delete("/{chat_id}/participants/{user_id}")
async def delete_participants_in_chat(chat_id: int, user_id: int, participant_service: ChatParticipantService = Depends(get_chat_participant_service), user=Depends(get_current_user)):
    return await participant_service.delete_participants_in_chat(chat_id, user.id, user_id)
