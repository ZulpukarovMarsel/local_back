from fastapi import APIRouter, Depends
from typing import List
from repositories import MessageRepository
from services import ChatParticipantService
from dependencies import get_current_user, get_message_repo, verify_participant, get_chat_participant_service
from schemas.message import MessageRead, MessageBase

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{chat_id}")
async def get_chat_messages(
    chat_id: int,
    limit: int = 20,
    offset: int = 0,
    message_repo: MessageRepository = Depends(get_message_repo),
    participant_service: ChatParticipantService = Depends(get_chat_participant_service),
    current_user=Depends(get_current_user),
):
    await participant_service.verify_user_in_chat(chat_id, current_user.id)
    messages = await message_repo.get_messages_by_chat_id(
        chat_id=chat_id,
        limit=limit,
        offset=offset,
    )
    return messages
