from app.user import schemas
import app.user.crud as user_crud
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user_by_id(user_id: int, db: Session):
    return user_crud.get_user_by_id(db, user_id)


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return user_crud.get_users(db, skip, limit)


def get_user_by_email(user: schemas.UserLogin, db: Session):
    return user_crud.get_user_by_email(db, user)


def create_user(user: schemas.UserCreate, db: Session):
    user.password = hash_password(user.password)
    return user_crud.create_user(db, user)


def update_user(user_id: int, user: schemas.UserUpdate, db: Session):
    return user_crud.update_user(db, user_id, user)


def delete_user(user_id: int, db: Session):
    return user_crud.delete_user(db, user_id)
