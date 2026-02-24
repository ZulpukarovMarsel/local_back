from .base_repository import BaseRepository
from models import Attachment


class AttachmentRepository(BaseRepository):
    model = Attachment
