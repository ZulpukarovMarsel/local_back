from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
    )


class CursorPageSchema(ORMBaseSchema, Generic[T]):
    items: list[T] = Field(default_factory=list)
    next_cursor: str | None = None
    has_more: bool = False


class OffsetPageSchema(ORMBaseSchema, Generic[T]):
    items: list[T] = Field(default_factory=list)
    limit: int
    offset: int
    total: int
    has_more: bool
