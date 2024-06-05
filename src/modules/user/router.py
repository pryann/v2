from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.service import UserService
from src.modules.user.schemas import UserRead, UserCreate, UserUpdate
from src.database.database import get_session
from src.modules.user.crud import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


async def get_existing_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserRead])
async def list_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def find_user(user_id: int, user: UserRead = Depends(get_existing_user_by_id)):
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    is_exists = await user_service.get_user_by_email(user.email)
    if is_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = await user_service.create_user(user)
    return new_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user: UserUpdate,
    existed_user: UserRead = Depends(get_existing_user_by_id),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id)
