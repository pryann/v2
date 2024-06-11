from typing import Type, TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy.sql.expression import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, sqlalchemy_model: Type[T]):
        self.session = session
        self.model = sqlalchemy_model

    async def get_by_id(self, obj_id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in: T) -> T:
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def delete(self, obj_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, obj_id: int, update_obj: T) -> T | None:
        obj = await self.get_by_id(obj_id)
        if obj:
            for key, value in update_obj.__dict__.items():
                setattr(obj, key, value)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        return None
