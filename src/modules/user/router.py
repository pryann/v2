from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from src.modules.user.service import UserService
from src.modules.user.schemas import UserReadSchema, UserCreateSchema, UserUpdateProfileSchema
from src.modules.user.utils import get_user_service


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


async def get_existing_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserReadSchema])
async def list_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_users()


@router.get("/{user_id}", response_model=UserReadSchema)
async def find_user(user_id: int, user: UserReadSchema = Depends(get_existing_user_by_id)):
    return user


@router.post("/", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    is_exists = await user_service.get_user_by_email(user.email)
    if is_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = await user_service.create_user(user)
    return new_user


@router.put("/{user_id}", response_model=UserReadSchema)
async def update_user(
    user_id: int,
    user: UserUpdateProfileSchema,
    existed_user: UserReadSchema = Depends(get_existing_user_by_id),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id)
