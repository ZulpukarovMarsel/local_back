from fastapi import APIRouter, Depends
from typing import List
from repositories import MessageRepository
from dependencies import get_current_user, get_message_repo, verify_participant
from schemas.message import MessageRead, MessageBase

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{chat_id}", response_model=List[MessageRead])
async def get_messages(chat_id: int, message_repo: MessageRepository = Depends(get_message_repo), verified=Depends(verify_participant)):
    return await message_repo.get_all_by_chat_id(chat_id)


@router.post("/{chat_id}", response_model=MessageRead)
async def create_message(data: MessageBase, chat_id: int, message_repo: MessageRepository = Depends(get_message_repo), user=Depends(get_current_user),  verified=Depends(verify_participant)):
    return await message_repo.create_data({"chat_id": chat_id, "sender_id": user.id, "content": data.content})


@router.delete("/{chat_id}/{message_id}")
async def delete_message(chat_id: int, message_id: int, message_repo: MessageRepository = Depends(get_message_repo),  verified=Depends(verify_participant)):
    return await message_repo.delete_data(message_id)
