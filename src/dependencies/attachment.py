from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import AttachmentRepository
from services import AttachmentService
from dependencies.db import get_db


async def get_attachment_repo(db: AsyncSession = Depends(get_db)):
    return AttachmentRepository(db)


async def get_attachment_service(attachment_repo: AttachmentRepository = Depends(get_attachment_repo)):
    return AttachmentService(attachment_repo)
