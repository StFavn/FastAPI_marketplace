from datetime import datetime

from pydantic import BaseModel


class SCommentRead(BaseModel):
    """Модель отображения покупки."""

    id:        int
    when:      datetime
    review_id: int
    user_id:   int
    content:   str


class SCommentCreate(BaseModel):
    """Модель для добавления покупки."""

    review_id: int
    content:   str

class SCommentUpdate(BaseModel):
    """Модель для обновления покупки."""

    content: str
