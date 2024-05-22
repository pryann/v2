from enum import Enum


class UserStatusEnum(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    BANNED = "BANNED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"
