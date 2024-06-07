from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user.service import UserService
from src.database.database import get_session
from src.modules.user.crud import UserRepository


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)
