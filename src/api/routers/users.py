import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

from services import ChatService, PostService

from repositories import UserRepository, UserFollowRepository
from models import PostType
from schemas.auth import (
    AuthProfileSchema
)
from schemas.message import MessageBase
from schemas.post import PostResponseSchema
# from schemas.post import PostReadSchema

from dependencies import get_user_repo, get_user_follow_repo, get_current_user, get_chat_service, get_post_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(lambda: None)]
)


@router.get("/", response_model=List[AuthProfileSchema], status_code=200)
async def get_users(
    user_repo: UserRepository = Depends(get_user_repo)
):
    return await user_repo.get_all()


@router.get("/{username}", response_model=AuthProfileSchema)
async def get_user(username: str, user_repo: UserRepository = Depends(get_user_repo)):
    return await user_repo.get_by_username(username)


# @router.get("/{username}/posts", response_model=List[PostReadSchema])
# async def get_user_posts(username: str, post_repo: PostRepository = Depends(get_post_repo)):
#     return await post_repo.get_data_by_username(username)


@router.get("/{username}/followers", response_model=None)
async def get_user_followers(username: str, user_follow_repo: UserFollowRepository = Depends(get_user_follow_repo)):
    return await user_follow_repo.get_user_followers(username)


@router.get("/{username}/followings", response_model=None)
async def get_user_followings(username: str, user_follow_repo: UserFollowRepository = Depends(get_user_follow_repo)):
    return await user_follow_repo.get_user_followings(username)


# TODO: 0.1.7 -  Подумать и сделать логику рек людей для пользователя на главной странице
@router.get("/suggestions", response_model=List[AuthProfileSchema])
async def get_suggestions(user_repo: UserRepository = Depends(get_user_repo)):
    return await user_repo.get_all()


@router.put("/{user_id}/follow", response_model=None)
async def user_follow(user_id: int, user_follow_repo: UserFollowRepository = Depends(get_user_follow_repo), user=Depends(get_current_user)):
    if user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Нельзя подписаться на самого себя",
        )

    follow = await user_follow_repo.get_data_by_follower_id_and_following_id(
        follower_id=user.id,
        following_id=user_id,
    )

    if follow:
        return follow

    return await user_follow_repo.create_data({"follower_id": user.id, "following_id": user_id})


@router.delete("/{user_id}/follow", response_model=None)
async def user_unfollow(user_id: int, user_follow_repo: UserFollowRepository = Depends(get_user_follow_repo), user=Depends(get_current_user)):
    return await user_follow_repo.unfollow(user.id, user_id)


@router.get("/{user_id}/follow-status", response_model=None)
async def user_follow_status(user_id: int, user_follow_repo: UserFollowRepository = Depends(get_user_follow_repo), user=Depends(get_current_user)):
    user_follow = await user_follow_repo.get_data_by_follower_id_and_following_id(user.id, user_id)
    if not user_follow:
        return False
    return True


@router.post("/{username}/message")
async def send_message_user(username: str, data: MessageBase, chat_service: ChatService = Depends(get_chat_service), user=Depends(get_current_user)):
    return await chat_service.create_private_chat(username, user.id, data)


@router.get("/{username}/reels", response_model=List[PostResponseSchema])
async def get_reels_user(username: str, request: Request, post_service: PostService = Depends(get_post_service)):
    return await post_service.get_user_content(username=username, base_url=str(request.base_url).rstrip("/"), content_type=PostType.REEL)


@router.get("/{username}/posts", response_model=List[PostResponseSchema])
async def get_posts_user(username: str, request: Request, post_service: PostService = Depends(get_post_service)):
    return await post_service.get_user_content(username=username, base_url=str(request.base_url).rstrip("/"), content_type=PostType.POST)
