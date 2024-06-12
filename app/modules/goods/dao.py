from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import GoodsModel
from .schemas import SGoodsRecalculate
from app.modules.reviews.models import ReviewModel



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
                    .options(selectinload(GoodsModel.reviews))
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
    
    @classmethod
    async def recalculate_rating(cls, goods_id: int):
        """Пересчет рейтинга товара с учетом всех отзывов."""

        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    select(func.sum(ReviewModel.rating), func.count(ReviewModel.id))
                    .where(ReviewModel.goods_id == goods_id)
                    .group_by(ReviewModel.goods_id)
                )

                result_execute = await session.execute(query)
                rating_sum, reviews_count = \
                    result_execute.one_or_none() or (None, None)
            

                if rating_sum is None or reviews_count == 0:
                    average_rating = None
                else:
                    average_rating = rating_sum / reviews_count


                update_data = SGoodsRecalculate(
                    average_rating=average_rating
                )

                updated_goods = await cls.update_object(
                    id=goods_id, update_data=update_data
                )

                if not updated_goods:
                    return None
                return updated_goods
