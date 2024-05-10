from sqlalchemy import Column,  ForeignKey, Integer, String, Boolean,Enum
from sqlalchemy.orm import relationship
from ..models import CustomBase
from ..consts import UserStatusEnum


class User(CustomBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(Enum(UserStatusEnum),default=UserStatusEnum.unverified.value, nullable=False)

    billing_addresses = relationship("BillingAddress", back_populates="user")
