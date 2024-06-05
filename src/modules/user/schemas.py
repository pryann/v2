from pydantic import BaseModel, EmailStr, Field, constr, field_validator
from typing import Annotated
from src.modules.user.consts import UserStatusEnum, UserRoleEnum

password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class UserBase(BaseModel):
    username: str
    newsletter_subscription: bool


class UserRead(UserBase):
    id: int
    email: EmailStr
    status: UserStatusEnum
    role: UserRoleEnum


class UserCreate(UserBase):
    email: EmailStr
    password: Annotated[str, constr(pattern=password_regex)]
    terms_accepted: bool = Field(..., description="Terms and conditions must be accepted")


class UserUpdateProfile(UserBase):
    pass


class UserUpdateEmail(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(pattern=password_regex)]


class UserUpdateStatus(BaseModel):
    status: UserStatusEnum


class UserUpdatePassword(BaseModel):
    old_password: Annotated[str, constr(pattern=password_regex)]
    new_password: Annotated[str, constr(pattern=password_regex)]
    # confirm_new_password: Annotated[str, constr(pattern=password_regex)]

    # @field_validator("confirm_new_password")
    # def passwords_match(cls, v, values):
    #     if "new_password" in values and v != values["new_password"]:
    #         raise ValueError("new_password and confirm_new_password do not match")
    #     return v
