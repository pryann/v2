from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta
import src.user.schemas as user_schemas
from src.config import get_settings
import src.auth.service as auth_service
from src.database import get_db
from sqlalchemy.orm import Session

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api",
    tags=["Auth"],
)


@router.post("/auth/login")
async def login(response: Response, user: user_schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(email=user.email, password=user.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_token(
        data={"sub": user.email},
        expires=access_token_expires,
        secret=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ACCESS_TOKEN_ALGORITHM,
    )

    # refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    # refresh_token = auth_service.create_token(
    #     data={"sub": user.email},
    #     expires=refresh_token_expires,
    #     secret=settings.REFRESH_TOKEN_SECRET_KEY,
    #     algorithm=settings.ACCESS_TOKEN_ALGORITHM,
    # )
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    # response.set_cookie(
    #     key="refresh_token", value=refresh_token, httponly=True, secure=True
    # )
    return {}


# Logout route
@router.get("/auth//logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {}


# Refresh token route
@router.post("/auth//refresh-tokens", response_model=dict)
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    is_valid_token = auth_service.verify_refresh_token(refresh_token)
    if not is_valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token data",
        )

    user: user_schemas.UserRead = auth_service.get_current_user_from_token(refresh_token)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_token(
        data={"sub": user.email},
        expires=access_token_expires,
        secret=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ACCESS_TOKEN_ALGORITHM,
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {}
