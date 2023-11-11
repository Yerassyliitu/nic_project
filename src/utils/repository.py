from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from settings.database_connection.connection import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, filters):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data) -> int:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def get_one(self, filters=None):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            return res

