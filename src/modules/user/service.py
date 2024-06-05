import bcrypt
from typing import List
from src.user.schemas import UserCreate, UserRead, UserUpdate
from src.user.crud import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _hash_password(password) -> bytes:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode("utf-8")
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

    async def get_users(self) -> List[UserRead]:
        return await self.user_repository.get_all(UserRead)

    async def get_user_by_id(self, user_id: int) -> UserRead:
        return await self.user_repository.get_by_id(user_id, UserRead)

    async def create_user(self, user_data: UserCreate) -> UserRead:
        user_data.password = self._hash_password(user_data.password)
        return await self.user_repository.add(user_data, UserRead)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserRead:
        return await self.user_repository.update(user_id, user_data, UserRead)

    async def delete_user(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)
