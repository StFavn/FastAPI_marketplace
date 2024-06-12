from typing import List
from fastapi import APIRouter, Depends

from app.exceptions import DatabaseErrorException, NotFoundException
from app.modules.users.manager import current_active_user
from app.modules.users.models import UserModel

from .dao import CartDAO
from .schemas import SCartCreate, SCartRead

router = APIRouter(
    prefix='/carts',
    tags=['carts']
)


@router.post('')
async def create_cart(
    data: SCartCreate, user: UserModel = Depends(current_active_user)
):
    """Добавляет товар в корзину."""
    cart = await CartDAO.add_cart_object(
        goods_id=data.goods_id,
        user_id=user.id
    )

    if not cart:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )

    return cart


@router.get('', response_model=List[SCartRead])
async def get_all_carts(user: UserModel = Depends(current_active_user)):
    """Возвращает все товары в корзине текущего пользователя."""
    carts = await CartDAO.get_all_objects(user_id=user.id)

    if not carts:
        raise NotFoundException
    return carts


@router.delete('/{cart_id}')
async def delete_cart(
    cart_id: int, user: UserModel = Depends(current_active_user)
):
    """Удаляет товар из корзины."""
    result = await CartDAO.delete_object(
        id=cart_id, user_id=user.id
    )

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result


@router.delete('')
async def delete_all_carts(user: UserModel = Depends(current_active_user)):
    """Удаляет все товары из корзины пользователя."""
    result = await CartDAO.delete_all_objects(user_id=user.id)

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
