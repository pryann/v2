from typing import TypeVar, Generic, List
from pydantic import BaseModel
from src.utils.base_repository import BaseRepository

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def get_all(self) -> List[T]:
        return await self.repository.get_all()

    async def get_by_id(self, obj_id: int) -> T | None:
        return await self.repository.get_by_id(obj_id)

    async def create(self, obj_in: T) -> T:
        return await self.repository.create(obj_in)

    async def update(self, obj_id: int, update_obj: T) -> T | None:
        return await self.repository.update(obj_id, update_obj)

    async def delete(self, obj_id: int) -> None:
        await self.repository.delete(obj_id)
