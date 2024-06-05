from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, orm
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.models import CustomBase
from typing import List


class BillingAddress(CustomBase):
    __tablename__ = "billing_address"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255))
    state: Mapped[int]
    city: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[str] = mapped_column(String(10))
    address: Mapped[str] = mapped_column(String(10))
    tax_number: Mapped[str] = mapped_column(String(10))
    outside_eu: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
