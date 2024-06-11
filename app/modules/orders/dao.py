from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import OrderModel


class OrderDAO(BaseDAO):
    model = OrderModel

    @classmethod
    async def add_order_object(
        cls,
        goods_id: int,
        user_id: int,
        status: str | None = 'accepted'
    ):
        """Добавление объекта покупки к заказу."""
        try:
            async with async_session_maker() as session:
                order = insert(OrderModel).values(
                    goods_id=goods_id, user_id=user_id, status=status
                ).returning(
                    OrderModel.id, 
                    OrderModel.when,
                    OrderModel.status,
                    OrderModel.goods_id, 
                    OrderModel.user_id
                )
                order = await session.execute(order)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return order.mappings().one()

    