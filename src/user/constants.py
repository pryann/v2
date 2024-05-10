from enum import Enum


class UserStatusEnum(str, Enum):
    unverified = 'unverified'
    verified = 'verified'
    banned = 'banned'
    blocked = 'blocked'
    deleted = 'deleted'
