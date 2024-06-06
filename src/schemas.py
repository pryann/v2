from pydantic import BaseModel, Field, field_validator


class MyModel(BaseModel):
    my_field: str = Field(...)

    @field_validator("my_field")
    def check_my_field(cls, v):
        if "invalid" in v:
            raise ValueError("my_field is invalid")
        return v
