from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.logger import logger

from .models import CommentModel

class CommentDAO(BaseDAO):
    model = CommentModel

    @classmethod
    async def add_comment_object(
        cls,
        review_id: int,
        user_id: int,
        content: str
    ):
        """Добавление объекта покупки к заказу."""
        try:
            async with async_session_maker() as session:
                comment = insert(CommentModel).values(
                    review_id=review_id, user_id=user_id, content=content
                ).returning(
                    CommentModel.id, 
                    CommentModel.when,
                    CommentModel.content,
                    CommentModel.review_id, 
                    CommentModel.user_id
                )
                comment = await session.execute(comment)
                await session.commit()
        except (SQLAlchemyError, Exception) as error:
            message = f'An error has occurred: {error}'
            logger.error(
                message,
                extra={'Database table': cls.model.__tablename__},
                exc_info=True
            )
            return None
        return comment.mappings().one()