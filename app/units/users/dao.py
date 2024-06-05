from app.dao.base import BaseDAO

from .models import UserModel

class UserDAO(BaseDAO):
    model = UserModel