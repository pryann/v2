from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import Settings, get_settings
from src.database.database import get_session
from src.utils.token_handler import TokenHandler
from src.modules.auth.schemas import LoginSchema
from src.modules.auth.service import AuthService
from src.modules.user.crud import UserRepository

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    user_repository = UserRepository(session)
    token_service = TokenHandler()
    return AuthService(user_repository=user_repository, token_handler=token_service, settings=settings)


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(response: Response, user: LoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    tokens = await auth_service.login(user)
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, secure=True)
    return {}


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {}


@router.get("/refresh-tokens", status_code=status.HTTP_204_NO_CONTENT)
async def refresh_tokens(response: Response, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    tokens = await auth_service.regenerate_tokens(refresh_token)
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, secure=True)
    return {}
