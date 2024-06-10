from typing import List
from fastapi import APIRouter, Depends

from app.modules.users.manager import current_superuser
from app.modules.users.models import UserModel

from .dao import CategoryDAO
from .schemas import SCategoryCreate, SCategoryRead, SCategoryUpdate

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.post('')
async def create_category(
    data: SCategoryCreate, user: UserModel = Depends(current_superuser)
):
    """Позволяет добавить новую категорию."""

    # TODO: Проверка на наличие категории
    # category_exists = await CategoryDAO.get_one(name=data.name)
    # if category_exists:
    #     raise ObjectAlreadyExistsException

    new_category = await CategoryDAO.create(**data.model_dump())

    # TODO: Проверка на успешное добавление
    # if not new_category:
    #     raise DatabaseErrorException(
    #         detail='Не удалось добавить запись в базу данных.'
    #     )

    return new_category


@router.get('', response_model=List[SCategoryRead])
async def get_all_categories():
    """Возвращает все категории."""
    categories = await CategoryDAO.get_all()

    # TODO: Проверка на успешное получение
    # if not categories:
    #     raise NotFoundException

    return categories


@router.get('/{category_id}', response_model=SCategoryRead)
async def get_category(category_id: int):
    """Возвращает конкретную категорию."""
    category = await CategoryDAO.get_one(id=category_id)

    # TODO: Проверка на успешное получение
    # if not category:
    #     raise NotFoundException

    return category


@router.patch('/{category_id}', response_model=SCategoryRead)
async def update_category(
    category_id: int,
    update_data: SCategoryUpdate,
    user: UserModel = Depends(current_superuser)
):
    """Позволяет обновить название категории."""

    category = await CategoryDAO.update(
        update_data=update_data, id=category_id
    )

    # TODO: Проверка на успешное обновление
    # if not category:
    #     raise DatabaseErrorException(detail='Не удалось обновить данные.')

    return category


@router.delete('/{category_id}')
async def delete_category(
    category_id: int, user: UserModel = Depends(current_superuser)
):
    """Позволяет удалить категорию."""
    result = await CategoryDAO.delete(id=category_id)

    # TODO: Проверка на успешное удаление
    # if not result:
    #     raise DatabaseErrorException(
    #         detail='Не удалось удалить запись из базы данных.'
    #     )
    
    return result


