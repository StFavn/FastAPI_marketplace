from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin

from app.config import settings

from .config import auth_backend
from .models import UserModel
from .utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = settings.PASSWORD
    verification_token_secret = settings.PASSWORD

    async def on_after_register(
        self, user: UserModel, request: Request | None = None
    ):
        print(f'Пользователь c id {user.id} был зарегистрирован.')

    async def on_after_forgot_password(
        self, user: UserModel, token: str, request: Request | None = None
    ):
        print(f'Пользователь с id {user.id} забыл свой пароль. '
              f'Токен сброса пароля: {token}')

    async def on_after_request_verify(
        self, user: UserModel, token: str, request: Request | None = None
    ):
        print(f'Запрошена верификация для пользователя с id {user.id}.'
              f'Токен верификации: {token}')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
