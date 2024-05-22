from pydantic import BaseModel, EmailStr, constr, Field
from typing import Annotated, Optional
from datetime import datetime
from app.user.consts import UserStatusEnum

password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class UserBase(BaseModel):
    username: str = Field(required=True, max_length=20)
    email: EmailStr

    class Config:
        orm_mode = True


class UserRead(UserBase):
    id: int
    status: UserStatusEnum
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str = Field(required=True, min_length=8, max_length=255)


class UserUpdate(UserBase):
    pass


class UserUpdateStatus(BaseModel):
    status: UserStatusEnum


class UserUpdatePassword(BaseModel):
    old_password: Annotated[str, constr(regex=password_regex)]
    new_password: Annotated[str, constr(regex=password_regex)]
    confirm_new_password: Annotated[str, constr(regex=password_regex)]
