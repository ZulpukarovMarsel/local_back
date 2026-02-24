from repositories.user import UserRepository
from repositories.role import RoleRepository
from repositories.otp import OTPRepository
from repositories.post import PostRepository
from repositories.attachment import AttachmentRepository
from repositories.comment import CommentRepository
from repositories.like import LikeRepository
from repositories.favorite import FavoriteRepository

__all__ = [
    "UserRepository",
    "RoleRepository",
    "OTPRepository",
    "PostRepository",
    "AttachmentRepository",
    "CommentRepository",
    "LikeRepository",
    "FavoriteRepository"
]
