from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RoleAddSchema(BaseModel):
    title: str


class RoleUpdateSchema(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None


class RoleSchema(RoleAddSchema):
    id: int
    title: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
