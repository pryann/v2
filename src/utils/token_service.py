from datetime import datetime

from src.config import Settings


class TokenService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate_token(self, user: LoginReadSchema, expires_delta: timedelta, secret_key: str, algorithm: str) -> str:
        expire = datetime.now(datetime.UTC) + expires_delta
        to_encode = {"id": user.id, "email": user.email, "role": user.role, "exp": expire}
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    def decode_token(self, token: str, secret_key: str, algorithm: str):
        return jwt.decode(token, secret_key, algorithms=[algorithm])