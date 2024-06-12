from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import Base

class CartModel(Base):
    """Модель покупки."""

    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    customer: Mapped['UserModel'] = relationship(back_populates='in_cart') # type: ignore

    def __str__(self):
        return f'Покупка:id - {self.id}, совершена - {self.when}'
    