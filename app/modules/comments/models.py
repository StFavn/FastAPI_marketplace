from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base_model import Base


class CommentModel(Base):
    """Модель комментария."""

    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    content: Mapped[str] = mapped_column(String(length=1000))
    review_id: Mapped[int] = mapped_column(ForeignKey('reviews.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    writer: Mapped['UserModel'] = relationship(back_populates='comments') # type: ignore
    review: Mapped['ReviewModel'] = relationship(back_populates='comments') # type: ignore

    def __str__(self):
        return f'Покупка:id - {self.id}, совершена - {self.when}'
    