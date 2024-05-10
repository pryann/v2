from pydantic import BaseModel


class BillingAddress(BaseModel):
    id: int
    name: str
    description: str