from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from schemas.common import ORMBaseSchema
from schemas.user import UserShortResponseSchema


class MessageCreateSchema(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )


class MessageUpdateSchema(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000,
    )


class MessageResponseSchema(ORMBaseSchema):
    id: int
    chat_id: int
    sender_id: int

    content: str
    sender: UserShortResponseSchema

    created_at: datetime
    updated_at: datetime


class ChatRoleCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    can_delete_messages: bool = False
    can_add_users: bool = False
    can_remove_users: bool = False
    can_edit_chat: bool = False
    can_change_roles: bool = False


class ChatRoleUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    can_delete_messages: bool | None = None
    can_add_users: bool | None = None
    can_remove_users: bool | None = None
    can_edit_chat: bool | None = None
    can_change_roles: bool | None = None


class ChatRoleResponseSchema(ORMBaseSchema):
    id: int
    chat_id: int
    name: str

    can_delete_messages: bool
    can_add_users: bool
    can_remove_users: bool
    can_edit_chat: bool
    can_change_roles: bool


class ChatParticipantCreateSchema(BaseModel):
    user_id: int
    chat_role_id: int | None = None


class ChatParticipantRoleUpdateSchema(BaseModel):
    chat_role_id: int


class ChatParticipantResponseSchema(ORMBaseSchema):
    id: int
    chat_id: int
    user_id: int
    chat_role_id: int

    user: UserShortResponseSchema
    chat_role: ChatRoleResponseSchema


class ChatCreateSchema(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=255,
    )

    is_group: bool = False
    participant_ids: list[int] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_participants(self):
        self.participant_ids = list(dict.fromkeys(self.participant_ids))

        if not self.is_group and len(self.participant_ids) != 1:
            raise ValueError(
                "Личный чат должен содержать одного другого участника"
            )

        if self.is_group and not self.name:
            raise ValueError(
                "Для группового чата необходимо указать название"
            )

        return self


class ChatUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class ChatListResponseSchema(ORMBaseSchema):
    id: int
    name: str
    is_group: bool

    participants: list[ChatParticipantResponseSchema] = Field(
        default_factory=list,
    )

    last_message: MessageResponseSchema | None = None
    unread_count: int = 0

    created_at: datetime
    updated_at: datetime


class ChatDetailResponseSchema(ChatListResponseSchema):
    chat_roles: list[ChatRoleResponseSchema] = Field(
        default_factory=list,
    )
