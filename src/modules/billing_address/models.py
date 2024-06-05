from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.database.models import CustomBase


class BillingAddress(CustomBase):
    __tablename__ = "billing_address"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[str] = mapped_column(String(10))
    address: Mapped[str] = mapped_column(String(288))
    tax_number: Mapped[str] = mapped_column(String(10))
    outside_eu: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
