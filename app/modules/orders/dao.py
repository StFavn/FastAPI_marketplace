from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import OrderModel
from app.modules.carts.models import CartModel

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
    

    @classmethod
    async def add_orders_from_cart(cls, user_id: int):
        """Позволяет добавить к покупке все товары из корзины и очистить корзину."""
        try:
            async with async_session_maker() as session:
                async with session.begin():  # Транзакция
                    query = select(CartModel).filter_by(user_id=user_id)
                    goods_in_cart_objects = await session.execute(query)
                    goods_in_cart = goods_in_cart_objects.scalars().all()

                    if not goods_in_cart:
                        raise Exception("Корзина пуста")
        
                    orders = []
                    for good in goods_in_cart:
                        order = OrderModel(
                            goods_id=good.goods_id,
                            user_id=user_id,
                            status='accepted'
                        )
                        session.add(order)
                        orders.append(order)
                    
                    # Удаление товаров из корзины
                    try: 
                        for good in goods_in_cart:
                            await session.delete(good)
                    except Exception as error:
                        raise error
                
                await session.commit()
                
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None

        return orders

    