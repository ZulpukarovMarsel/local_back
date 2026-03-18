import logging
from typing import List
from fastapi import APIRouter, Depends, Query

from repositories import UserRepository
from schemas.user import (
    UserReadSchema
)
from services import ChatService
from schemas.message import MessageBase
from dependencies import get_user_repo, get_current_user, get_chat_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(lambda: None)]
)


@router.get("/", response_model=List[UserReadSchema], status_code=200)
async def get_users(
    user_repo: UserRepository = Depends(get_user_repo)
):
    return await user_repo.get_all()


@router.post("/{username}/message")
async def send_message_user(username: str, data: MessageBase, chat_service: ChatService = Depends(get_chat_service), user=Depends(get_current_user)):
    return await chat_service.create_private_chat(username, user.id, data)


@router.get("/users/search", response_model=List[UserReadSchema])
async def search_users(
    q: str = Query(..., description="Username для поиска"),
    user_repo: UserRepository = Depends(get_user_repo)
):
    return await user_repo.search_by_username(q)
