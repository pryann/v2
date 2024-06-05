from typing import List
from sqlalchemy import Enum, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.modules.user.consts import UserStatusEnum, UserRoleEnum
from src.database.models import CustomBase
from src.modules.billing_address.models import BillingAddress


class User(CustomBase):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    terms_accepted: Mapped[bool] = mapped_column(Boolean)
    newsletter_subscription: Mapped[bool] = mapped_column(Boolean)
    password: Mapped[bytes] = mapped_column(String(255))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.USER.value,
    )
    status: Mapped[UserStatusEnum] = mapped_column(
        Enum(UserStatusEnum),
        default=UserStatusEnum.UNVERIFIED.value,
    )

    billing_address: Mapped[List["BillingAddress"]] = relationship(lazy="selectin")
