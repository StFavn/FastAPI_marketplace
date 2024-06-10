from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    """Класс для работы с переменными окружения."""

    MODE: Literal['DEV', 'TEST', 'PROD', 'INFO', 'DEBUG']
    LOG_LEVEL: str

    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_PG_DB_NAME: str
    TEST_PG_HOST: str
    TEST_PG_PORT: int
    TEST_PG_USER: str
    TEST_PG_PASSWORD: str


    SECRET_KEY: str
    ALGORITHM: str

    SECRET: str
    PASSWORD: str

    @property
    def DATABASE_URL(self):
        if self.MODE == 'DEV':
            return (f'postgresql+asyncpg://{self.POSTGRES_USER}:'
                    f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                    f'{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}')
        elif self.MODE == 'TEST':
            return (f'postgresql+asyncpg://{self.TEST_PG_USER}:'
                    f'{self.TEST_PG_PASSWORD}@{self.TEST_PG_HOST}:'
                    f'{self.TEST_PG_PORT}/{self.TEST_PG_DB_NAME}')

    # для локальной разработки
    model_config = SettingsConfigDict(env_file='.env')

    # для запуска в docker
    # model_config = SettingsConfigDict(env_file='.env-docker')

settings = Settings()
