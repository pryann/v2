from humps import camel
from sqlalchemy import Column, func, DateTime
from app.database import Base


def to_camel(string):
    return camel(string)


class CustomBase(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
