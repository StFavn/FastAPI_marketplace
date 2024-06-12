from datetime import datetime

from pydantic import BaseModel


class SReviewRead(BaseModel):
    """Модель отображения ревью."""

    id:           int
    goods_id:     int
    user_id:      int
    rating:       int
    when:         datetime
    positive_msg: str | None = None
    negative_msg: str | None = None
    verdict_msg:  str



class SReviewCreate(BaseModel):
    """Модель для добавления ревью."""

    goods_id:     int
    rating:       int
    positive_msg: str | None = None
    negative_msg: str | None = None
    verdict_msg:  str
    

class SReviewUpdate(BaseModel):
    """Модель для обновления ревью."""

    rating:       int | None = None
    positive_msg: str | None = None
    negative_msg: str | None = None
    verdict_msg:  str | None = None
   
