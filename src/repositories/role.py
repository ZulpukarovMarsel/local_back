from sqlalchemy import select

from repositories.base_repository import BaseRepository
from models import Role


class RoleRepository(BaseRepository):
    model = Role

    async def get_by_ids(self, ids: list[int]):
        if not ids:
            return []
        result = await self.db.execute(
            select(self.model)
            .where(self.model.id.in_(ids))
        )
        return list(result.unique().scalars().all())
