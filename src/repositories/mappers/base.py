from typing import TypeVar

from pydantic import BaseModel
from src.utils.database import BaseModel as DBBaseModel

DBModelType = TypeVar('DBModelType', bound=DBBaseModel)
SchemaType = TypeVar('SchemaType', bound=BaseModel)

class DataMapper:
    db_model: type(DBModelType) = None # Модель SQLAlchemy
    schema: type(SchemaType) = None   # Pydantic схема

    @classmethod
    def map_to_domain_entity(cls, data):
        '''Конвертирует SQLAlchemy объект в Pydantic схему'''
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        '''Конвертирует Pydantic схему в SQLAlchemy объект'''
        return cls.db_model(**data.model_dump())