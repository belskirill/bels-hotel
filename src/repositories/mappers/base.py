from typing import TypeVar

from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    # из алхимии в pydantic схему
    @classmethod
    def map_to_domain(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    # из pydantic схемы в модель алхимии
    def map_to_persistence_enity(cls, data):
        return cls.db_model(**data.model_dump())
