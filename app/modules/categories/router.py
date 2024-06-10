from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, Query
# from fastapi_cache.decorator import cache

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.modules.users.manager import current_superuser
from app.modules.users.models import UserModel

from .dao import CategoryDAO
from .schemas import (
    SCategoryCreate,
    SCategoryGoodsRead,
    SCategoryRead,
    SCategoryUpdate
)

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.post('')
async def create_category(
    data: SCategoryCreate, user: UserModel = Depends(current_superuser)
):
    """Создание новой категории."""

    # Проверка на наличие категории
    category_exists = await CategoryDAO.get_object(name=data.name)
    if category_exists:
        raise ObjectAlreadyExistsException

    new_category = await CategoryDAO.add_object(**data.model_dump())

    # Проверка на успешное добавление
    if not new_category:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )

    return new_category


@router.get('', response_model=List[SCategoryRead])
async def get_all_categories():
    """Возврат всех категорий."""
    categories = await CategoryDAO.get_all_objects()

    # Проверка на успешное получение
    if not categories:
        raise NotFoundException

    return categories


@router.get('/{category_id}', response_model=SCategoryRead)
async def get_category(category_id: int):
    """Возвращение категории по id"""
    category = await CategoryDAO.get_object(id=category_id)

    # Проверка на успешное получение
    if not category:
        raise NotFoundException

    return category


@router.patch('/{category_id}', response_model=SCategoryRead)
async def update_category(
    category_id: int,
    update_data: SCategoryUpdate,
    user: UserModel = Depends(current_superuser)
):
    """Обновление названия категории."""

    category = await CategoryDAO.update_object(
        update_data=update_data, id=category_id
    )

    # Проверка на успешное обновление
    if not category:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')

    return category


@router.delete('/{category_id}')
async def delete_category(
    category_id: int, user: UserModel = Depends(current_superuser)
):
    """Удаление каатегории."""
    result = await CategoryDAO.delete_object(id=category_id)

    # Проверка на успешное удаление
    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    
    return result


@router.get('/{category_id}/goods', response_model=List[SCategoryGoodsRead])
# @cache(expire=60)
async def get_all_category_goods(
        category_id: int,
        date: date = Query(default=datetime.now().date())
    ):
        """Возвращает список всех товаров категории."""
        category_goods = await CategoryDAO.get_all_category_goods_objects(
            category_id=category_id,
            date=date,
        )

        if not category_goods:
            raise NotFoundException
        return category_goods