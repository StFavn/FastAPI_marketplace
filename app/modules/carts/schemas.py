from pydantic import BaseModel


class SCartRead(BaseModel):
    """Модель отображения покупки в корзине."""

    id: int
    goods_id: int
    user_id: int


class SCartCreate(BaseModel):
    """Модель для добавления покупки в корзину."""

    goods_id: int

