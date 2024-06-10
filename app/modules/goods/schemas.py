from typing import Optional

from pydantic import BaseModel


class GoodsRead(BaseModel):
    """Модель отображения товара."""

    id:             int
    name:           str
    description:    str | None = None
    price:          int
    on_stock:       bool
    average_rating: float | None = None
    category_id:    int
    # image_id:       int


class GoodsCreate(BaseModel):
    """Модель для добавления товара."""

    name:           str
    description:    str | None = None
    price:          int
    on_stock:       bool
    category_id:    int
    # image_id:       int


class GoodsUpdate(BaseModel):
    """Модель для обновления товара."""

    name:           str | None = None
    description:    str | None = None
    price:          str | None = None
    on_stock:       bool | None = None
    category_id:    str | None = None
    # image_id:       str | None = None
