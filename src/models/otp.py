from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String

from models.base_model import Base


class OTP(Base):
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return f"<OTP(id={self.id}, email={self.email}, code={self.code})>"
