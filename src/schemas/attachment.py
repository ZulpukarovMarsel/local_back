from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AttachmentBaseSchema(BaseModel):
    file_path: str = Field(..., min_length=1)
    file_type: str = Field(..., min_length=1)


class AttachmentCreateSchema(AttachmentBaseSchema):
    post_id: int


class AttachmentUpdateSchema(BaseModel):
    file_path: Optional[str] = Field(None, min_length=1)
    file_type: Optional[str] = Field(None, min_length=1)


class AttachmentReadSchema(AttachmentBaseSchema):
    id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)
