from typing import Optional, List
from datetime import datetime
from enum import Enum
from typing_extensions import Self
from pydantic import BaseModel, model_validator, ConfigDict, EmailStr, Field
from fastapi import HTTPException, UploadFile, Form, File
from .roles import RoleSchema


class AuthProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None

    roles: List[RoleSchema] = Field(default_factory=list)

    posts_count: Optional[int] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuthProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[UploadFile] = None
    roles: Optional[List[RoleSchema]] = None


class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class AuthLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


class AuthRegisterSchema(AuthLoginSchema):
    username: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class AuthChangePasswordSchema(BaseModel):
    old_password: str
    password: str

    @model_validator(mode='after')
    def check_password(self) -> Self:
        if self.old_password == self.password:
            raise HTTPException(status_code=400, detail="Старый пароль и новый пароль похожи")
        return self


class AuthForgotPasswordSchema(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class AuthResetPasswordSchema(BaseModel):
    email: EmailStr
    code: int
    new_password: str

    class Config:
        from_attributes = True


class AuthTokenSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class AuthTokenDataSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class AuthTokenRefreshSchema(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True


class AuthTokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class OTPSchema(BaseModel):
    email: EmailStr


class OTPCheckSchema(BaseModel):
    email: EmailStr
    code: int

    class Config:
        from_attributes = True


class OTPPurpose(str, Enum):
    register = "register"
    reset_password = "reset_password"
