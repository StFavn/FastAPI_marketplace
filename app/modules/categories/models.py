# from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base_model import Base


class CategoryModel(Base):
    """Модель категории."""

    __tablename__ = 'categories'

    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=150))
    # image_id: Mapped[Optional[int]] = mapped_column(ForeignKey('images.id'))
    # goods: Mapped[List['GoodsModel']] = relationship(
    #     back_populates='category'
    # )

    def __str__(self):
        return f'Категория:id - {self.id}, название - {self.name}'