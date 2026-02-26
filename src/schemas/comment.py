from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class CommentBaseSchema(BaseModel):
    post_id: int
    parent_id: Optional[int] = None
    text: str = Field(..., min_length=1)


class CommentCreateSchema(BaseModel):
    parent_id: Optional[int] = None
    text: str = Field(..., min_length=1)


class CommentUpdateSchema(BaseModel):
    text: Optional[str] = Field(None, min_length=1)


class CommentReadSchema(CommentBaseSchema):
    id: int
    author_id: int

    replies: List["CommentReadSchema"] = []

    model_config = ConfigDict(from_attributes=True)


CommentReadSchema.model_rebuild()
