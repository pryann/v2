from enum import Enum
from typing import Annotated
from pydantic import constr


class UserStatusEnum(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    BANNED = "BANNED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class UserRoleEnum(str, Enum):
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    USER = "USER"
    TEACHER = "TEACHER"
    SPONSORE = "SPONSORE"


password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
PasswordType = Annotated[str, constr(pattern=password_regex)]
