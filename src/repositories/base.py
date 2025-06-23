from httpx import delete
from pydantic import BaseModel
from sqlalchemy import select, insert, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()


    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)  # Возвращает добавленный объект в виде pydantic - схемы
        )
        result = await self.session.execute(add_stmt)
        return result.scalars().one()


    async def update(self, data: BaseModel, **filter_by) -> None:
        upd_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
            .returning(self.model)
        )
        await self.session.execute(upd_stmt)


    async def delete(self, **filter_by) -> None:
        del_stmt = select(self.model).filter_by(**filter_by)
        for_delete = await self.session.execute(del_stmt)
        for record in for_delete.scalars().all():
            await self.session.delete(record)