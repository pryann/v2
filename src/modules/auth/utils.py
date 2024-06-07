from fastapi import Depends
import jwt
from types import Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import Settings, get_settings
from src.database.database import get_session
from src.utils.token_handler import TokenHandler
from src.modules.auth.service import AuthService
from src.modules.user.crud import UserRepository
from datetime import datetime, timedelta, timezone
from src.modules.user.schemas import LoginReadSchema


class TokenHandler:
    def generate_token(self, user: LoginReadSchema, expires_delta: timedelta, secret_key: str, algorithm: str) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"id": user.id, "email": user.email, "role": user.role, "exp": expire}
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    def decode_token(self, token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
        return jwt.decode(token, secret_key, algorithms=[algorithm])


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    user_repository = UserRepository(session)
    token_service = TokenHandler()
    return AuthService(user_repository=user_repository, token_handler=token_service, settings=settings)
