from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from slugify import slugify

from models.association_tables import user_role
from models.base_model import Base


class Role(Base):
    title: Mapped[str] = mapped_column()
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    users: Mapped[List["User"]] = relationship(secondary=user_role, back_populates="roles")

    def __init__(self, **kw):
        super().__init__(**kw)
        if not self.slug and self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"<Role(id={self.id}, title={self.title})>"
