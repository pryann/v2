from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, orm
from ..models import CustomBase


class BillingAddress(CustomBase):
    __tablename__ = "billing_address"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    state = Column(Integer)
    city = Column(String(255), nullable=False)
    zip_code = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    tax_number = Column(String(255))
    outside_eu = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = orm.relationship("User", back_populates="billing_addresses")
