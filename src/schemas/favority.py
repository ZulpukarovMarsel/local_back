from pydantic import BaseModel, ConfigDict


class FavoriteCreateSchema(BaseModel):
    post_id: int


class FavoriteReadSchema(BaseModel):
    id: int
    user_id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)
