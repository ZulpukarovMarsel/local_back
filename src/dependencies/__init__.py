from dependencies.user import get_user_repo, get_user_service, get_current_user, get_current_user_raw
from dependencies.auth import get_auth_service, get_profile_update_data
from dependencies.db import get_db
from dependencies.otp import get_otp_repo, get_otp_service
from dependencies.role import get_role_repo
from dependencies.post import get_post_repo, get_post_service
from dependencies.attachment import get_attachment_repo, get_attachment_service

__all__ = [
    "get_db",

    "get_user_repo",
    "get_user_service",
    "get_current_user",
    "get_current_user_raw",

    "get_otp_repo",
    "get_otp_service",

    "get_auth_service",
    "get_profile_update_data",

    "get_role_repo",

    "get_post_repo",
    "get_post_service",

    "get_attachment_repo",
    "get_attachment_service"
]
