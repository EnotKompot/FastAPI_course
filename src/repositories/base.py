from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete, tuple_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.exceptions import ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_all_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return model
        return self.mapper.map_to_domain_entity(model)


    async def get_one(self, **filter_by):
        query = (select(self.model).filter_by(**filter_by))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)


    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)  # Возвращает добавленный объект в виде pydantic - схемы
        )
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def update(self, data: BaseModel, **filter_by) -> None:
        upd_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump())
            .returning(self.model)
        )
        await self.session.execute(upd_stmt)

    async def update_particular(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        upd_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(upd_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def delete_bulk(self, delete_data: list[BaseModel]):
        keys = tuple(delete_data[0].model_dump().keys())

        values_to_delete = [tuple(getattr(item, field) for field in keys) for item in delete_data]
        where_condition = tuple_(*[getattr(self.model, field) for field in keys]).in_(
            values_to_delete
        )

        delete_stmt = delete(self.model).where(where_condition)
        await self.session.execute(delete_stmt)
