from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Annotated
from src.modules.user.consts import UserStatusEnum

password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class UserBase(BaseModel):
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class UserRead(UserBase):
    id: int
    status: UserStatusEnum


class UserCreate(UserBase):
    password: Annotated[str, constr(pattern=password_regex)]


class UserUpdate(UserBase):
    pass


class UserLogin(UserCreate):
    pass


class UserUpdateStatus(BaseModel):
    status: UserStatusEnum

    class Config:
        from_attributes = True


class UserUpdatePassword(BaseModel):
    old_password: Annotated[str, constr(pattern=password_regex)]
    new_password: Annotated[str, constr(pattern=password_regex)]
    confirm_new_password: Annotated[str, constr(pattern=password_regex)]

    @field_validator("confirm_new_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("new_password and confirm_new_password do not match")
        return v

    class Config:
        from_attributes = True
