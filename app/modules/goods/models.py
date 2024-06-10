from typing import List, Optional

from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import Base

class GoodsModel(Base):
    """Модель товара."""

    __tablename__ = 'goods'
    
    id:             Mapped[int] = mapped_column(primary_key=True)
    name:           Mapped[str] = mapped_column(String(length=250))
    description:    Mapped[Optional[str]] = mapped_column(String(length=500))
    price:          Mapped[int]
    average_rating: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    on_stock:       Mapped[bool]

    category_id:    Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    category: Mapped['CategoryModel'] = relationship(back_populates='goods') # type: ignore
    # image_id: Mapped[Optional[int]] = mapped_column(ForeignKey('images.id'))
    # orders: Mapped[List['OrdersModel']] = relationship(back_populates='goods')
    # reviews: Mapped[List['ReviewModel']] = relationship(back_populates='goods')

    def __str__(self):
        return f'Товар:id - {self.id}, название - {self.name}'
