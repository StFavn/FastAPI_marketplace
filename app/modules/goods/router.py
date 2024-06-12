from typing import List

from fastapi import APIRouter, Depends

from app.exceptions import (
    DatabaseErrorException,
    NotFoundException,
    ObjectAlreadyExistsException
)
from app.modules.users.manager import current_superuser
from app.modules.users.models import UserModel

from .dao import GoodsDAO
from .schemas import SGoodsCreate, SGoodsRead, SGoodsUpdate

router = APIRouter(
    prefix='/goods',
    tags=['goods']
)


@router.post('')
async def create_goods(
    data: SGoodsCreate, user: UserModel = Depends(current_superuser)
):
    """Добавление нового товара."""

    goods_exists = await GoodsDAO.get_object(name=data.name)
    if goods_exists:
        raise ObjectAlreadyExistsException
    
    new_goods = await GoodsDAO.add_object(**data.model_dump())
    if not new_goods:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return new_goods


@router.post('/recalculate_rating')
async def recalculate_rating(goods_id: int):
    """Пересчет рейтинга товара с учетом всех отзывов."""

    updated_goods = await GoodsDAO.recalculate_rating(goods_id=goods_id)

    if not updated_goods:
        raise DatabaseErrorException(
            detail='Не удалось обновить данные в базе данных.'
        )
    return updated_goods


@router.get('/{goods_id}', response_model=SGoodsRead)
async def get_good(goods_id: int):
    """Возвращение товара по id."""

    goods = await GoodsDAO.get_object(id=goods_id)
    if not goods:
        raise NotFoundException
    return goods


@router.get('', response_model=List[SGoodsRead])
async def get_goods():
    """Возвращение всех товаров."""

    goods = await GoodsDAO.get_all_objects()
    if not goods:
        raise NotFoundException
    return goods


@router.get('_all')
async def get_goods_all_information(
    user: UserModel = Depends(current_superuser)
):
    """Возвращает все товары cо всей информацией."""
    goods = await GoodsDAO.get_goods_objects_all_information()

    if not goods:
        raise NotFoundException
    return goods


@router.patch('/{goods_id}', response_model=SGoodsRead)
async def update_goods(
    goods_id: int,
    update_data: SGoodsUpdate,
    user: UserModel = Depends(current_superuser)
):
    """Обновление данных товара."""

    goods = await GoodsDAO.update_object(
        update_data=update_data, id=goods_id
    )

    if not goods:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return goods


@router.delete('/{goods_id}')
async def delete_goods(
    goods_id: int, user: UserModel = Depends(current_superuser)
):
    """Удаление товара."""

    result = await GoodsDAO.delete_object(id=goods_id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
