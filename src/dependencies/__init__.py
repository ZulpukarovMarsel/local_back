from dependencies.user import get_user_repo, get_user_service
from dependencies.auth import get_auth_service
from dependencies.db import get_db
from dependencies.otp import get_otp_repo, get_otp_service
from dependencies.role import get_role_repo

__all__ = [
    "get_db",
    "get_user_repo",
    "get_otp_repo",
    "get_otp_service",
    "get_user_service",
    "get_auth_service",
    "get_role_repo"
]
