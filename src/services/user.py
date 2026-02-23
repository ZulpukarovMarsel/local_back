
from passlib.context import CryptContext
from typing import Any
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from services.base_service import BaseService
from repositories import UserRepository, RoleRepository
from schemas.auth import AuthProfileSchema, AuthProfileUpdateSchema
from models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserService(BaseService):
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    # async def create_user(self, user_data):
    #     user_data = user_data.copy()
    #     user_data['password'] = self.hash_password(user_data['password'])
    #     return await self.user_repo.create_data(user_data)

    async def update_user(self, user_id: int, data: dict[str, Any]) -> User | None:
        user = await self.user_repo.get_data_by_id(user_id)
        if not user:
            return None

        for key in ("email", "first_name", "last_name", "password"):
            if key in data:
                val = data[key]
                if key == "password" and val:
                    val = self.hash_password(val)
                setattr(user, key, val)

        if "roles" in data:
            role_ids = list(dict.fromkeys(data["roles"]))
            roles = await self.role_repo.get_by_ids(role_ids)
            user.roles = roles

        try:
            await self.user_repo.db.flush()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        except SQLAlchemyError:
            raise

        return user

    async def patch_user(self, user_id: int, data: dict):
        user = await self.user_repo.get_data_by_id(user_id)
        if not user:
            return None
        if "password" in data and data["password"]:
            user.password = self.hash_password(data["password"])
        if "roles" in data:
            roles = await self.role_repo.get_by_ids(list(dict.fromkeys(data["roles"])))
            user.roles = roles
        for k, v in data.items():
            if k in {"password", "roles"}:
                continue
            setattr(user, k, v)
        try:
            await self.user_repo.db.flush()
            await self.user_repo.db.refresh(user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        except SQLAlchemyError:
            raise

        return user

    async def update_profile(self, user_id: int, data: AuthProfileUpdateSchema, base_url: str):
        update_data = data.dict(exclude_unset=True)

        update_data.pop("avatar", None)

        if data.avatar:
            avatar_info = await BaseService.upload_image(data.avatar, "avatars")
            update_data["avatar"] = avatar_info["image_path"]

        user = await self.patch_user(user_id, update_data)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if getattr(user, "avatar", None):
            user.avatar = f"{base_url}{user.avatar}"

        return AuthProfileSchema.model_validate(user)
