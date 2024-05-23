from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import app.user.service as user_service
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    user = user_service.get_user_by_email(email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_token(data: dict, expires: timedelta, secret: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.now(datetime.UTC) + expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def get_current_user_from_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[settings.ACCESS_TOKEN_ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    return user_service.get_user_by_email(email)


def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[settings.REFRESH_TOKEN_ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    return user_service.get_user_by_email(email)
