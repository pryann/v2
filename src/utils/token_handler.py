from datetime import datetime, timedelta, timezone
from src.modules.user.schemas import LoginReadSchema
import jwt
from types import Any


class TokenHandler:
    def generate_token(self, user: LoginReadSchema, expires_delta: timedelta, secret_key: str, algorithm: str) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {"id": user.id, "email": user.email, "role": user.role, "exp": expire}
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    def decode_token(self, token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
