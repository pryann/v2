from app import models
from app.user import schemas, models
import app.user.crud as user_crud
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return user_crud.get_user_by_id(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return user_crud.get_users(db, skip, limit)


def create_user(db: Session, user: schemas.UserCreate):
    return user_crud.create_user(db, user)


def update_user(
    db: Session, user: models.User, user_update: schemas.UserUpdate
):
    return user_crud.update_user(db, user, user_update)


def delete_user(db: Session, user_id: int):
    return user_crud.delete_user(db, user_id)
