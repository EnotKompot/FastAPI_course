from sqlalchemy import select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
        query = select(HotelsORM)
        if title:
            query = (
                query
                .where(HotelsORM.title.ilike(f"%{title.strip()}%"))
            )
        if location:
            query = (
                query
                .where(HotelsORM.location.ilike(f"%{location.strip()}%"))
            )

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()