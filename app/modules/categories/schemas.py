from pydantic import BaseModel

class SCategoryRead(BaseModel):
    """Схема отображения категории."""

    id:   int
    name: str
    # image_id: int


class SCategoryCreate(BaseModel):
    """Схема для добавления категории."""

    name: str
    # image_id: int


class SCategoryUpdate(BaseModel):
    """Схема для обновления категории."""

    name:     str | None = None
    image_id: int | None = None
