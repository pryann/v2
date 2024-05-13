from fastapi import APIRouter, HTTPException, status
from src.user.schemas import User
import src.user.service as user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "User Not Found Error"}},
)


@router.get("/")
async def list_users():
    return user_service.get_users()


@router.get("/{user_id}", response_model=User)
async def find_user(user_id: int):
    user = user_service.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_service.create_user(user)
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    existing_user = user_service.get_user(user_id)
    if existing_user:
        user_service.update_user(user)
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    existing_user = user_service.get_user(user_id)
    if existing_user:
        user_service.create_user(user_id)
    raise HTTPException(status_code=404, detail="User not found")
