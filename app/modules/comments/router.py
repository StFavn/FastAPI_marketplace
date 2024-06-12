from typing import List
from fastapi import APIRouter, Depends

from app.exceptions import DatabaseErrorException, NotFoundException
from app.modules.users.manager import current_active_user
from app.modules.users.models import UserModel

from .dao import CommentDAO
from .schemas import SCommentCreate, SCommentRead, SCommentUpdate

router = APIRouter(
    prefix='/comments',
    tags=['comments']
)


@router.post('')
async def create_comment(
    data: SCommentCreate, user: UserModel = Depends(current_active_user)
):
    """Позволяет добавить новый комментарий."""
    comment = await CommentDAO.add_comment_object(
        review_id=data.review_id,
        user_id=user.id,
        content=data.content
    )

    if not comment:
        raise DatabaseErrorException(
            detail='Не удалось добавить запись в базу данных.'
        )
    return comment


@router.get('/users/me', response_model=List[SCommentRead])
async def get_all_comments(user: UserModel = Depends(current_active_user)):
    """Возвращает все комментарии текущего пользователя."""
    comments = await CommentDAO.get_all_objects(user_id=user.id)

    if not comments:
        raise NotFoundException
    return comments


@router.get('/users/{user_id}', response_model=List[SCommentRead])
async def get_all_comments(user_id: int):
    """Возвращает все комментарии конкретного пользователя."""
    comments = await CommentDAO.get_all_objects(user_id=user_id)

    if not comments:
        raise NotFoundException
    return comments


@router.get('/reviews/{review_id}', response_model=List[SCommentRead])
async def get_all_comments(review_id: int):
    """Возвращает все комментарии конкретного отзыва."""
    comments = await CommentDAO.get_all_objects(review_id=review_id)

    if not comments:
        raise NotFoundException
    return comments


@router.get('/{comment_id}', response_model=SCommentRead)
async def get_comment(
    comment_id: int, user: UserModel = Depends(current_active_user)
):
    """Возвращает конкретный комментарий текущего пользователя."""
    comment = await CommentDAO.get_object(id=comment_id, user_id=user.id)

    if not comment:
        raise NotFoundException
    return comment


@router.patch('/{comment_id}', response_model=SCommentRead)
async def update_comment(
    comment_id: int,
    update_data: SCommentUpdate,
    user: UserModel = Depends(current_active_user)
):
    """Обновление данных товара текущего пользователя."""

    comment = await CommentDAO.update_object(
        update_data=update_data, id=comment_id, user_id=user.id
    )

    if not comment:
        raise DatabaseErrorException(detail='Не удалось обновить данные.')
    return comment


@router.delete('/{comment_id}')
async def delete_comment(
    comment_id: int, user: UserModel = Depends(current_active_user)
):
    """Позволяет удалить комментарий текущего пользователя."""
    result = await CommentDAO.delete_object(
        id=comment_id, user_id=user.id
    )

    if not result:
        raise DatabaseErrorException(
            detail='Не удалось удалить запись из базы данных.'
        )
    return result