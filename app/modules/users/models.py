from datetime import date
from typing import Optional, List

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func # для использования SQL-функции CURRENT_DATE

from app.database.base_model import Base


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id:              Mapped[int] = mapped_column(primary_key=True)
    username:        Mapped[str] = mapped_column(String(length=50))
    first_name:      Mapped[Optional[str]] = mapped_column(String(length=100))
    last_name:       Mapped[Optional[str]] = mapped_column(String(length=150))
    email:           Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    registrated:     Mapped[date] = mapped_column(default=func.current_date())
    is_active:       Mapped[bool] = mapped_column(default=True)
    is_superuser:    Mapped[bool] = mapped_column(default=False)
    is_verified:     Mapped[bool] = mapped_column(default=False)

    # image_id: Mapped[Optional[int]] = mapped_column(ForeignKey('images.id'))
    orders: Mapped[List['OrderModel']] = relationship( # type: ignore
        back_populates='buyer', cascade='all, delete-orphan'
    )
    in_cart: Mapped[List['CartModel']] = relationship( # type: ignore
        back_populates='customer', cascade='all, delete-orphan'
    )
    reviews: Mapped[List['ReviewModel']] = relationship( # type: ignore
        back_populates='reviewer', cascade='all, delete-orphan'
    )
    comments: Mapped[List['CommentModel']] = relationship( # type: ignore
        back_populates='writer', cascade='all, delete-orphan'
    )
    
    def __str__(self):
        return f'Пользователь:id - {self.id}, username - {self.username}'
