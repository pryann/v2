import jwt
import bcrypt
from datetime import timedelta
from src.config import Settings
from src.exceptions.exceptions import NotFoundError, AuthencticationError
from src.modules.auth.schemas import LoginSchema, LoginReadSchema
from src.modules.user.crud import UserRepository
from src.utils.token_handler import TokenHandler


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        token_handler: TokenHandler,
        settings: Settings,
    ):
        self.user_repository = user_repository
        self.token_service = token_handler
        self.settings = settings

    def _generate_access_token(self, user: LoginReadSchema) -> str:
        return self.token_service.generate_token(
            user,
            timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            self.settings.ACCESS_TOKEN_SECRET_KEY,
            self.settings.ACCESS_TOKEN_ALGORITHM,
        )

    def _generate_refresh_token(self, user: LoginReadSchema) -> str:
        return self.token_service.generate_token(
            user,
            timedelta(minutes=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            self.settings.REFRESH_TOKEN_SECRET_KEY,
            self.settings.REFRESH_TOKEN_ALGORITHM,
        )

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def _get_current_user_from_access_token(self, access_token: str) -> LoginReadSchema:
        decoded = self.token_service.decode_token(
            access_token, self.settings.ACCESS_TOKEN_SECRET_KEY, self.settings.ACCESS_TOKEN_ALGORITHM
        )
        return await self.user_repository.get_user_by_email(decoded["email"])

    async def regenerate_tokens(self, refresh_token: str) -> dict[str, str]:
        decoded = self.token_service.decode_token(
            refresh_token, self.settings.REFRESH_TOKEN_SECRET_KEY, self.settings.REFRESH_TOKEN_ALGORITHM
        )
        user = await self.user_repository.get_user_by_email(decoded["email"])
        return {
            "access_token": self._generate_access_token(user),
            "refresh_token": self._generate_refresh_token(user),
        }

    async def login(self, user: LoginSchema) -> dict[str, str]:
        db_user = await self.user_repository.get_by_email(user.email)
        if not db_user:
            raise NotFoundError("User not found")
        if not self._verify_password(user.password, db_user.password):
            raise AuthencticationError("Incorrect email or password")
        return {
            "access_token": self._generate_access_token(db_user),
            "refresh_token": self._generate_refresh_token(db_user),
        }
