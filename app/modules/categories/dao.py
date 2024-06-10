from fastapi import Query
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import CategoryModel
from app.modules.goods.models import GoodsModel

class CategoryDAO(BaseDAO):
    model = CategoryModel

    @classmethod
    async def get_all_category_goods_objects(
        cls,
        category_id: int,
        date: date
    ):
        """Возвращение списка всех товаров категории и их наличия на складе"""
        
        try:
            async with async_session_maker() as session:
                get_goods = (
                    select(GoodsModel, *GoodsModel.__table__.columns)
                    .where(GoodsModel.category_id == category_id)
                )

                all_category_goods = await session.execute(get_goods)
                return all_category_goods.mappings().all()
            
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={
                    'subcategory_id': category_id,
                    'date': date
                },
                exc_info=True
            )
            return None