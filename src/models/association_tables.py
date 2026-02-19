from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from models.base_model import Base


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)
