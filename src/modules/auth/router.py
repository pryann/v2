from fastapi import APIRouter, Depends, status, Response, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.modules.auth.utils import get_auth_service
from src.modules.auth.utils import get_auth_service
from src.modules.auth.schemas import LoginSchema
from src.modules.auth.service import AuthService


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit()
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
