from typing import List
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.user.consts import UserStatusEnum
from src.models import CustomBase
from src.billing_address.models import BillingAddress


class User(CustomBase):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    status: Mapped[UserStatusEnum] = mapped_column(
        Enum(UserStatusEnum),
        default=UserStatusEnum.UNVERIFIED.value,
    )
    billing_address: Mapped[List["BillingAddress"]] = relationship(lazy="selectin")
