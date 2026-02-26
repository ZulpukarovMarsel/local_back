from dependencies.user import get_user_repo, get_user_service, get_current_user, get_current_user_raw
from dependencies.auth import get_auth_service, get_profile_update_data
from dependencies.db import get_db
from dependencies.otp import get_otp_repo, get_otp_service
from dependencies.role import get_role_repo
from dependencies.post import get_post_repo, get_post_service
from dependencies.attachment import get_attachment_repo, get_attachment_service
from dependencies.comment import get_comment_repo, get_comment_service
from dependencies.like import get_like_repo
from dependencies.favorite import get_favorite_repo

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
    "get_attachment_service",

    "get_comment_repo",
    "get_comment_service",

    "get_like_repo",

    "get_favorite_repo"
]
