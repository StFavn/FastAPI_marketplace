from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import GoodsModel
from app.modules.categories.models import CategoryModel



class GoodsDAO(BaseDAO):
    model = GoodsModel

    @classmethod
    async def get_goods_objects_all_information(cls, **kwargs):
        """Возвращение всех товаров с полной информацией."""

        try:
            async with async_session_maker() as session:
                goods = (
                    select(GoodsModel)
                    .options(selectinload(GoodsModel.orders))
                    .options(joinedload(GoodsModel.category))
                )
                goods = await session.execute(goods)
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return jsonable_encoder(goods.scalars().all())
