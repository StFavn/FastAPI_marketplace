from app.dao.base import BaseDAO

from .models import CategoryModel

class CategoryDAO(BaseDAO):
    model = CategoryModel
