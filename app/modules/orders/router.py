from typing import List

from fastapi import APIRouter, Depends


from app.exceptions import DatabaseErrorException, NotFoundException
from app.modules.users.manager import current_active_user
from app.modules.users.models import UserModel

from .dao import OrderDAO
from .schemas import SOrderCreate, SOrderRead

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.post('')
async def create_order(
    data: SOrderCreate, user: UserModel = Depends(current_active_user)
):
    """Позволяет добавить новую покупку."""
    order = await OrderDAO.add_order_object(
        goods_id=data.goods_id,
        user_id=user.id
    )

    if not order:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )


    return order


@router.get('', response_model=List[SOrderRead])
async def get_all_orders(user: UserModel = Depends(current_active_user)):
    """Возвращает все покупки текущего пользователя."""
    orders = await OrderDAO.get_all_objects(user_id=user.id)

    if not orders:
        raise NotFoundException
    return orders


@router.get('/{order_id}', response_model=SOrderRead)
async def get_order(
    order_id: int, user: UserModel = Depends(current_active_user)
):
    """Возвращает конкретную покупку текущего пользователя."""
    order = await OrderDAO.get_object(id=order_id, user_id=user.id)

    if not order:
        raise NotFoundException
    return order


@router.delete('/{order_id}')
async def delete_order(
    order_id: int, user: UserModel = Depends(current_active_user)
):
    """Позволяет пользователю удалить/отменить покупку."""
    result = await OrderDAO.delete_object(
        id=order_id, user_id=user.id
    )

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result
