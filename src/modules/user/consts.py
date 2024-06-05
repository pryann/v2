from enum import Enum


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