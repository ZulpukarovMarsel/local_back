from fastapi import Depends

from services import AuthService, UserService
from repositories import UserRepository
from dependencies.user import get_user_repo, get_user_service


async def get_auth_service(user_repo: UserRepository = Depends(get_user_repo), user_service: UserService = Depends(get_user_service)):
    return AuthService(user_repo, user_service)
