from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict
from schemas.message import MessageRead


class ChatParticipantBase(BaseModel):
    user_ids: List[int]


class ChatParticipantCreate(ChatParticipantBase):
    pass


class ChatParticipantRead(ChatParticipantBase):
    model_config = ConfigDict(from_attributes=True)


class ChatBase(BaseModel):
    name: str
    is_group: bool = False


class ChatCreateSchema(ChatBase):
    participant_ids: List[int]


class ChatRead(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime
    participants: List[ChatParticipantRead] = []
    messages: List[MessageRead] = []

    model_config = ConfigDict(from_attributes=True)
