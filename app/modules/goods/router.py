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
from .schemas import GoodsCreate, GoodsRead, GoodsUpdate

router = APIRouter(
    prefix='/goods',
    tags=['goods']
)


@router.post('')
async def create_goods(
    data: GoodsCreate, user: UserModel = Depends(current_superuser)
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


@router.get('', response_model=List[GoodsRead])
async def get_goods():
    """Возвращение всех товаров."""

    goods = await GoodsDAO.get_all_objects()
    if not goods:
        raise NotFoundException
    return goods





@router.get('/{goods_id}', response_model=GoodsRead)
async def get_good(goods_id: int):
    """Возвращение товара по id."""

    goods = await GoodsDAO.get_object(id=goods_id)
    if not goods:
        raise NotFoundException
    return goods


@router.patch('/{goods_id}', response_model=GoodsRead)
async def update_goods(
    goods_id: int,
    update_data: GoodsUpdate,
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

@router.get('_all')
async def get_goods_all_information(
    user: UserModel = Depends(current_superuser)
):
    """Возвращает все товары cо всей информацией."""
    goods = await GoodsDAO.get_goods_objects_all_information()

    if not goods:
        raise NotFoundException
    return goods