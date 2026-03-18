from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class MessageCreateSchema(MessageBase):
    chat_id: int
    sender_id: int


class MessageRead(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
