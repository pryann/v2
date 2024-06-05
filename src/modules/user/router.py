from fastapi import APIRouter, HTTPException, status, Depends
from src.user import schemas, service
from src.database import get_db
from sqlalchemy.orm import Session
from typing import List
import src.email.service as EmailService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


async def get_user_service(session: AsyncSession = Depends(get_session)):
    user_repository = UserRepository(session)
    return UserService(user_repository)


async def get_existing_user_by_id(user_id: int, db: Session):
    user = service.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/",
    response_model=List[schemas.UserRead],
    response_model_exclude_unset=True,
)
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_users(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=schemas.UserRead,
    response_model_exclude_unset=True,
)
async def find_user(user_id: int, db: Session = Depends(get_db)):
    return get_existing_user_by_id(user_id, db)


@router.post(
    "/",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    is_exists = service.get_user_by_email(user.email, db)
    if is_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = service.create_user(user, db)
    EmailService.send_html_email(new_user.email, new_user.name)
    return new_user


@router.put(
    "/{user_id}",
    response_model=schemas.UserRead,
    response_model_exclude_unset=True,
)
async def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    get_existing_user_by_id(user_id, db)
    return service.update_user(user_id, user, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    get_existing_user_by_id(user_id, db)
    service.delete_user(user_id, db)