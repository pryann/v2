from pydantic import EmailStr
from src.modules.user.consts import UserRoleEnum
from src.utils.base_schema import BaseSchema


class LoginSchema(BaseSchema):
    email: EmailStr
    password: str


class LoginReadSchema(BaseSchema):
    id: int
    username: str
    password: str
    role: UserRoleEnum
