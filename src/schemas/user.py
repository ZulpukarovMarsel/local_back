from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=6)


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)


class UserReadSchema(UserBaseSchema):
    id: int
    roles: List[str] = []

    model_config = ConfigDict(from_attributes=True)
