from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import ReviewModel


class ReviewDAO(BaseDAO):
    model = ReviewModel

    @classmethod
    async def add_review_object(
        cls,
        goods_id:     int,
        user_id:      int,
        rating:       int | None = None,
        positive_msg: str | None = None,
        negative_msg: str | None = None,
        verdict_msg:  str | None = None
    ):
        """Добавление объекта покупки к заказу."""
        try:
            async with async_session_maker() as session:
                review = insert(ReviewModel).values(
                    goods_id=goods_id, 
                    user_id=user_id, 
                    rating=rating,
                    positive_msg=positive_msg,
                    negative_msg=negative_msg,
                    verdict_msg=verdict_msg,
                ).returning(
                    ReviewModel.id, 
                    ReviewModel.when,
                    ReviewModel.goods_id, 
                    ReviewModel.user_id,
                    ReviewModel.rating,
                    ReviewModel.positive_msg,
                    ReviewModel.negative_msg,
                    ReviewModel.verdict_msg
                )
                review = await session.execute(review)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return review.mappings().one()

    