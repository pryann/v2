from typing import Type
from pydantic import BaseModel


def convert_to_model(obj: BaseModel, schema_type: Type[BaseModel]) -> BaseModel | None:
    return schema_type.model_config(obj) if obj else None
