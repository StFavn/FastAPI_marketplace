from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import CartModel

class CartDAO(BaseDAO):
    model = CartModel

    @classmethod
    async def add_cart_object(
        cls,
        goods_id: int,
        user_id: int,
    ):
        """Добавление объекта покупки к заказу."""
        try:
            async with async_session_maker() as session:
                cart = insert(CartModel).values(
                    goods_id=goods_id, user_id=user_id
                ).returning(
                    CartModel.id, 
                    CartModel.goods_id, 
                    CartModel.user_id
                )
                cart = await session.execute(cart)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return cart.mappings().one()



    