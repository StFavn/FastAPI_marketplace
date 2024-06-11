from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base_model import Base


class OrderModel(Base):
    """Модель покупки."""

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    status: Mapped[str] = mapped_column(String(length=50))
    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    buyer: Mapped['UserModel'] = relationship(back_populates='orders') # type: ignore
    goods: Mapped['GoodsModel'] = relationship(back_populates='orders') # type: ignore

    def __str__(self):
        return f'Покупка:id - {self.id}, совершена - {self.when}'
