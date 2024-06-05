import bcrypt
from typing import List
from src.modules.user.schemas import UserCreate, UserRead, UserUpdate
from src.modules.user.crud import UserRepository
from src.database.database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.models import User
from src.utils.base_service import BaseService
from src.utils.convert_to_model import convert_to_model


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _hash_password(self, password) -> bytes:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode("utf-8")
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    async def get_users(self) -> List[UserRead]:
        return await self.user_repository.get_all()

    async def get_user_by_id(self, user_id: int) -> UserRead:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> UserRead:
        return await self.user_repository.get_by_email(email)

    async def create_user(self, user_data: UserCreate) -> UserRead:
        user_data.password = self._hash_password(user_data.password).decode("utf-8")
        return await self.user_repository.create(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserRead:
        return await self.user_repository.update(user_id, user_data)

    async def delete_user(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)
