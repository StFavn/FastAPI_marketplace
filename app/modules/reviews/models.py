from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base_model import Base


class ReviewModel(Base):
    """Модель покупки."""

    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    positive_msg: Mapped[Optional[str]] = mapped_column(String(length=1000))
    negative_msg: Mapped[Optional[str]] = mapped_column(String(length=1000))
    verdict_msg: Mapped[str] = mapped_column(String(length=1000))
    rating: Mapped[int]

    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    reviewer: Mapped['UserModel'] = relationship(back_populates='reviews') # type: ignore
    goods: Mapped['GoodsModel'] = relationship(back_populates='reviews') # type: ignore
    # comments: Mapped[List['CommentModel']] = relationship(back_populates='review') # type: ignore

    def __str__(self):
        return f'Ревью:id - {self.id}, написано - {self.when}'
