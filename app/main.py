# импорт из стандартной библиотеки
from fastapi import FastAPI
import contextlib

# импорт собственных утилит
from app.logger import logger

# Modules routing
from app.modules.categories.router import router as categories_router
from app.modules.goods.router import router as goods_router
from app.modules.orders.router import router as orders_router
from app.modules.reviews.router import router as reviews_router
from app.modules.carts.router import router as carts_router
# from app.modules.comments.router import router as comments_router

# User routing
from app.modules.users.config import auth_backend
from app.modules.users.manager import fastapi_users
from app.modules.users.schemas import SUserCreate, SUserRead, SUserUpdate

app = FastAPI(
    title='marketplace'
)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'Service {app.title} STARTUP.')
    try:
        yield
    finally:
        logger.info(f'Service {app.title} SHUTDOWN')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(SUserRead, SUserCreate),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_verify_router(SUserRead),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_users_router(
        SUserRead, SUserUpdate, requires_verification=True
    ),
    prefix='/users',
    tags=['users'],
)

app.include_router(categories_router)
app.include_router(goods_router)
app.include_router(orders_router)
app.include_router(reviews_router)
app.include_router(carts_router)
# app.include_router(comments_router)