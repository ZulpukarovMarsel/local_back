from sqlalchemy import select, delete

from repositories.base_repository import BaseRepository
from models import OTP


class OTPRepository(BaseRepository):
    model = OTP

    async def get_by_email_code_purpose(self, email: str, code: int, purpose: str):
        result = await self.db.execute(
            select(self.model).where(
                self.model.email == email,
                self.model.code == code,
                self.model.purpose == purpose,
            )
        )
        return result.scalar_one_or_none()

    async def delete_by_email_purpose(self, email: str, purpose: str):
        await self.db.execute(
            delete(self.model).where(
                self.model.email == email,
                self.model.purpose == purpose,
            )
        )
