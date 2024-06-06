from src.database.base_repository import BaseRepository
from src.modules.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user
