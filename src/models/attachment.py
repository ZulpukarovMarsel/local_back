from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from models.base_model import Base


class Attachment(Base):
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="attachments")

    file_path: Mapped[str] = mapped_column(nullable=False)
    file_type: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Attachment(id={self.id}, type={self.file_type})>"
