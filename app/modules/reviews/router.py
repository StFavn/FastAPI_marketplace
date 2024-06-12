from typing import List

from fastapi import APIRouter, Depends

from app.exceptions import DatabaseErrorException, NotFoundException
from app.modules.users.manager import current_active_user
from app.modules.users.models import UserModel

from .dao import ReviewDAO
from .schemas import SReviewCreate, SReviewRead, SReviewUpdate


router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@router.post('')
async def create_review(
    data: SReviewCreate, user: UserModel = Depends(current_active_user)
):
    """Добавление нового отзыва."""
    review = await ReviewDAO.add_review_object(
        goods_id=data.goods_id,
        user_id=user.id,
        rating=data.rating,
        positive_msg=data.positive_msg,
        negative_msg=data.negative_msg,
        verdict_msg=data.verdict_msg
    )

    if not review:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )

    return review


@router.get('/me', response_model=List[SReviewRead])
async def get_all_reviews(user: UserModel = Depends(current_active_user)):
    """Возврат всех отзывов текущего пользователя."""
    reviews = await ReviewDAO.get_all_objects(user_id=user.id)

    if not reviews:
        raise NotFoundException
    return reviews


@router.get('/users/{user_id}', response_model=List[SReviewRead])
async def get_all_reviews_by_user(user_id: int):
    """Возврат всех отзывов конкретного пользователя."""
    reviews = await ReviewDAO.get_all_objects(user_id=user_id)

    if not reviews:
        raise NotFoundException
    return reviews


@router.get('/goods/{goods_id}', response_model=List[SReviewRead])
async def get_all_reviews_by_goods(goods_id: int):
    """Возврат всех отзывов конкретного товара."""
    reviews = await ReviewDAO.get_all_objects(goods_id=goods_id)

    if not reviews:
        raise NotFoundException
    return reviews


@router.get('/{review_id}', response_model=SReviewRead)
async def get_review(review_id: int):
    """Возвращает конкретный отзыв."""
    review = await ReviewDAO.get_object(id=review_id)

    if not review:
        raise NotFoundException
    return review


@router.patch('/{review_id}', response_model=SReviewRead)
async def update_review(
    review_id: int,
    update_data: SReviewUpdate,
    user: UserModel = Depends(current_active_user)
):
    """Позволяет пользователю изменить свой отзыв."""
    review = await ReviewDAO.update_object(
        update_data=update_data, 
        id=review_id, 
        user_id=user.id
    )

    if not review:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return review


@router.delete('/{review_id}')
async def delete_review(
    review_id: int, user: UserModel = Depends(current_active_user)
):
    """Позволяет пользователю удалить свой отзыв."""
    result = await ReviewDAO.delete_object(
        id=review_id, user_id=user.id
    )

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result


