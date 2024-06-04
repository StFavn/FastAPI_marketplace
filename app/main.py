from fastapi import FastAPI

from app.logger import logger

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