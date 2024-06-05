# импорт из стандартной библиотеки
from fastapi import FastAPI

from app.logger import logger

from app.modules.users.config import auth_backend
from app.modules.users.manager import fastapi_users
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate

def lifespan(app: FastAPI):
    logger.info(f'Service {app.title} STARTUP.')
    yield
    logger.info(f'Service {app.title} SHUTDOWN')

app = FastAPI(
    title='marketplace',
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
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
        UserRead, UserUpdate, requires_verification=True
    ),
    prefix='/users',
    tags=['users'],
)

