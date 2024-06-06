# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta, timezone
# import src.modules.user.service as user_service
# from src.config import get_settings
# from sqlalchemy.orm import Session
#
#
# settings = get_settings()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def verify_password(plain_password, hashed_password) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def authenticate_user(email: str, password: str, db: Session):
#     user = user_service.get_user_by_email(email, db)
#     if not user or not verify_password(password, user.password):
#         return None
#     return user
#
#
# def create_token(data: dict, expires: timedelta, secret: str, algorithm: str) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + expires
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
#     return encoded_jwt
#
#
# def get_current_user_from_token(token: str):
#     try:
#         payload = jwt.decode(
#             token,
#             settings.ACCESS_TOKEN_SECRET_KEY,
#             algorithms=[settings.ACCESS_TOKEN_ALGORITHM],
#         )
#         email = payload.get("sub")
#         if email is None:
#             return None
#     except JWTError:
#         return None
#     return user_service.get_user_by_email(email)
#
#
# def verify_refresh_token(refresh_token: str):
#     try:
#         payload = jwt.decode(
#             refresh_token,
#             settings.REFRESH_TOKEN_SECRET_KEY,
#             algorithms=[settings.REFRESH_TOKEN_ALGORITHM],
#         )
#         email = payload.get("sub")
#         if email is None:
#             return None
#     except JWTError:
#         return None
#     return True
