from sqlalchemy import String
from src.models import CustomBase
from src.consts import UserStatusEnum
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from typing import List
from src.billing_address.models import BillingAddress


class User(CustomBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    status: Mapped[UserStatusEnum] = mapped_column(
        UserStatusEnum,
        default=UserStatusEnum.unverified.value,
    )
    billing_address: Mapped[List["BillingAddress"]] = relationship(lazy="selectin")
