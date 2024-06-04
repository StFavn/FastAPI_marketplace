from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import async_session_maker
from app.logger import logger

class BaseDAO:
    """Класс для работы с объектами БД."""

    model = None

    @classmethod
    async def get_one(cls, **kwargs):
        """Возвращение одного объекта модели из БД."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result.mappings().one_or_none()
    
    @classmethod
    async def get_all(cls, **kwargs):
        """Возвращение всех объектов модели из БД."""
        try:
            async with async_session_maker() as session:
                query = (select(cls.model.__table__.columns)
                         .filter_by(**kwargs)
                         .order_by(cls.model.id))
                result = await session.execute(query)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result.mappings().all()
    
    @classmethod
    async def create(cls, **kwargs):
        """Добавление объекта в БД."""
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return 'Данные успешно добавлены.'
    
    @classmethod
    async def update(cls, update_data, **kwargs):
        """Обновление данных объекта в БД."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar_one_or_none()
                new_data = update_data.dict(exclude_unset=True)

                for key, value in new_data.items():
                    setattr(result, key, value)
                session.add(result)
                await session.commit()
                await session.refresh(result)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return result
    
    @classmethod
    async def delete(cls, **kwargs):
        """Удаление объекта из БД."""
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar_one_or_none()
                await session.delete(result)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return 'Удаление успешно завершено.'