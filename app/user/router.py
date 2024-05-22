from fastapi import APIRouter, HTTPException, status, Depends
from app.user import schemas, service
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=List[schemas.UserRead],
    response_model_exclude_unset=True,
)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return service.get_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{user_id}",
    response_model=schemas.UserRead,
    response_model_exclude_unset=True,
)
async def find_user(user_id: int, db: Session = Depends(get_db)):
    try:
        existing_user = service.get_user_by_id(db, user_id)
        if existing_user:
            return existing_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_unset=True,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return service.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{user_id}",
    response_model=schemas.UserRead,
    response_model_exclude_unset=True,
)
async def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    try:
        updated_user = service.update_user(db, user_id, user)
        if updated_user:
            return updated_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        if not service.delete_user(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
