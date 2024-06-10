from datetime import date
from typing import Optional, List

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func # для использования SQL-функции CURRENT_DATE

from app.database.base_model import Base


class UserModel(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя.

Параметры relationship:  
back_populates='buyer': Этот параметр указывает, что на стороне объекта Purchase также существует отношение, 
которое ссылается на объект User. Поле buyer в модели Purchase будет использоваться для обратной связи. 
Это позволяет двустороннюю навигацию между пользователем и его покупками.  
cascade='all, delete-orphan': Каскадные параметры управляют тем, как операции сессии 
(такие как добавление, удаление и обновление) распространяются от родительского объекта 
(в данном случае User) на связанные дочерние объекты (в данном случае Purchase).  

Опции каскада:
all: Применяет все каскадные действия.
delete-orphan: Указывает, что если объект Purchase больше не связан с объектом User 
(например, пользователь удален), то и Purchase также должен быть удален из базы данных.

Наследование:
Совместимость с FastAPI Users: Наследование от SQLAlchemyBaseUserTable 
обеспечивает совместимость с fastapi-users, что позволяет легко использовать его функциональность 
для регистрации, аутентификации и управления пользователями.  

"""
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
    # purchases: Mapped[List['PurchaseModel']] = relationship(
    #     back_populates='buyer', cascade='all, delete-orphan'
    # )
    # reviews: Mapped[List['ReviewModel']] = relationship(
    #     back_populates='user', cascade='all, delete-orphan'
    # )
    # comments: Mapped[List['CommentModel']] = relationship(
    #     back_populates='user', cascade='all, delete-orphan'
    # )
    # in_cart: Mapped[List['CartModel']] = relationship(
    #     back_populates='user', cascade='all, delete-orphan'
    # )
    
    def __str__(self):
        return f'Пользователь:id - {self.id}, username - {self.username}'
