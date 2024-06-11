from datetime import datetime

from pydantic import BaseModel


class SOrderRead(BaseModel):
    """Модель отображения покупки."""

    id:       int
    when:     datetime
    goods_id: int
    user_id:  int
    status:   str


class SOrderCreate(BaseModel):
    """Модель для добавления покупки."""

    goods_id: int
    status:   str | None = 'accepted'
