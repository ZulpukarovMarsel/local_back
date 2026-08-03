from fastapi import Depends, Form, File, UploadFile
from pydantic import EmailStr
from typing import Optional

from services import AuthService, UserService
from repositories import UserRepository
from dependencies.user import get_user_repo, get_user_service
from schemas.auth import AuthProfileUpdateSchema


async def get_auth_service(user_repo: UserRepository = Depends(get_user_repo), user_service: UserService = Depends(get_user_service)):
    return AuthService(user_repo, user_service)


async def get_profile_update_data(
    avatar: Optional[UploadFile] = File(None),
    username: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
):
    return AuthProfileUpdateSchema(
        avatar=avatar,
        username=username,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        email=email,
    )
