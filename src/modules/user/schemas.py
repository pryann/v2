from pydantic import EmailStr, Field, constr
from typing import Annotated
from src.modules.user.consts import UserStatusEnum, UserRoleEnum
from src.utils.basse_schema import BaseSchema

password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
PasswordType = Annotated[str, constr(pattern=password_regex)]


class UserBaseSchema(BaseSchema):
    username: str
    newsletter_subscription: bool


class UserReadSchema(UserBaseSchema):
    id: int
    email: EmailStr
    status: UserStatusEnum
    role: UserRoleEnum


class UserCreateSchema(UserBaseSchema):
    email: EmailStr
    password: Annotated[str, constr(pattern=password_regex)]
    terms_accepted: bool = Field(..., description="Terms and conditions must be accepted")


class UserUpdateProfileSchema(BaseSchema):
    username: str
    newsletter_subscription: bool


class UserUpdateEmailSchema(BaseSchema):
    email: EmailStr
    password: PasswordType


class UserUpdateStatusSchema(BaseSchema):
    status: UserStatusEnum


class UserUpdatePasswordSchema(BaseSchema):
    old_password: PasswordType
    new_password: PasswordType
