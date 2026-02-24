from services.base_service import BaseService
from repositories import AttachmentRepository


class AttachmentService(BaseService):
    def __init__(self, attachment_repo: AttachmentRepository):
        self.attachment_repo = attachment_repo
