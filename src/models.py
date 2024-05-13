from humps import camel
from sqlalchemy import Column, func, DateTime
from src.database import Base


def to_camel(string):
    return camel(string)


class CustomBase(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.current_timestamp(), nullable=False)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
