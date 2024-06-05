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

    async def _get_obj(self, obj_id: int):
        return await self.session.get(self.model, obj_id)

    async def get_by_id(self, obj_id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in: T) -> T:
        obj = self.model(**obj_in.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> None:
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self, obj_id: int, update_obj: T) -> T | None:
        obj = await self._get_obj(obj_id)
        if obj:
            for key, value in update_obj.model_dump().items():
                setattr(obj, key, value)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        return None


# class BaseRepository:
#     def __init__(self, session: AsyncSession, sqlalchemy_model: Type):
#         self.session = session
#         self.model = sqlalchemy_model

#     async def _get_obj(self, obj_id: int):
#         return await self.session.get(self.model, obj_id)

#     async def _convert_to_model(self, obj: BaseModel, schema_type: Type[BaseModel]) -> BaseModel | None:
#         return schema_type.model_config(obj) if obj else None

#     async def get_by_id(self, obj_id: int, read_schema_type: Type[BaseModel]) -> BaseModel | None:
#         stmt = select(self.model).where(self.model.id == obj_id)
#         result = await self.session.execute(stmt)
#         obj = result.scalars().first()
#         return self._convert_to_model(obj, read_schema_type)

#     async def get_all(self, read_schema_type: Type[BaseModel]) -> List[BaseModel]:
#         stmt = select(self.model)
#         result = await self.session.execute(stmt)
#         objs = result.scalars().all()
#         return [self._convert_to_model(obj, read_schema_type) for obj in objs]

#     async def add(self, obj_in: BaseModel, read_schema_type: Type[BaseModel]) -> BaseModel:
#         obj = self.model(**obj_in.model_dump())
#         self.session.add(obj)
#         await self.session.commit()
#         await self.session.refresh(obj)
#         return self._convert_to_model(obj, read_schema_type)

#     async def delete(self, obj_id: int) -> None:
#         stmt = delete(self.model).where(self.model.id == obj_id)
#         await self.session.execute(stmt)
#         await self.session.commit()

#     async def update(
#         self, obj_id: int, update_schema_type: BaseModel, read_schema_type: Type[BaseModel]
#     ) -> BaseModel | None:
#         obj = await self._get_obj(obj_id)
#         if obj:
#             for key, value in update_schema_type.model_dump().items():
#                 setattr(obj, key, value)
#             self.session.add(obj)
#             await self.session.commit()
#             await self.session.refresh(obj)
#             return self._convert_to_model(obj, read_schema_type)
#         return None
