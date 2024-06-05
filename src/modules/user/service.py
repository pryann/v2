import bcrypt
from typing import List
from src.modules.user.schemas import UserCreate, UserRead, UserUpdateProfile
from src.modules.user.crud import UserRepository
from src.utils.base_service import BaseService
from src.exceptions.exceptions import NotFoundError


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
        hashed_password_byte_enc = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_byte_enc)

    async def get_users(self) -> List[UserRead]:
        return await self.user_repository.get_all()

    async def get_user_by_id(self, user_id: int) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> UserRead:
        return await self.user_repository.get_by_email(email)

    async def create_user(self, user_data: UserCreate) -> UserRead:
        user_data.password = self._hash_password(user_data.password).decode("utf-8")
        return await self.user_repository.create(user_data)

    async def update_user(self, user_id: int, user_data: UserUpdateProfile) -> UserRead:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return await self.user_repository.update(user_id, user_data)

    async def delete_user(self, user_id: int) -> None:
        await self.user_repository.delete(user_id)
