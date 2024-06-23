from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.config import Settings, get_settings
from src.database.pg_database import get_session
from src.exceptions.custom_exceptions import AuthenticationError
from src.modules.auth.service import AuthService
from src.modules.auth.utils import TokenHandler
from src.modules.user.consts import UserRoleEnum
from src.modules.user.crud import UserRepository


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    user_repository = UserRepository(session)
    token_service = TokenHandler()
    return AuthService(user_repository=user_repository, token_handler=token_service, settings=settings)


def require_auth(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise AuthenticationError()
    user = auth_service.token_handler.get_current_user_from_access_token(access_token)
    if not user:
        raise AuthenticationError()
    return user


def require_role(
    request: Request,
    accepted_roles: list[str] = None,
    auth_service: AuthService = Depends(get_auth_service),

):
    if accepted_roles is None:
        accepted_roles = [UserRoleEnum.USER.value]
    user = require_auth(request, auth_service)
    if user.role not in accepted_roles:
        raise AuthenticationError()
    return user


# def require_auth(auth_service: AuthService = Depends(get_auth_service)):
#     def decorator(func):
#         async def wrapper(*args, **kwargs):
#             request: Request = kwargs.get("request")
#             access_token = request.cookies.get("access_token")
#             if not access_token:
#                 raise AuthenticationError()
#             user = auth_service.token_handler.get_current_user_from_access_token(access_token)
#             if not user:
#                 raise AuthenticationError()
#             return await func(*args, **kwargs)

#         return wrapper

#     return decorator


