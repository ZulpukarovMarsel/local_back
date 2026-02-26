from pydantic import BaseModel, ConfigDict


class LikeCreateSchema(BaseModel):
    post_id: int


class LikeReadSchema(BaseModel):
    id: int
    author_id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)
