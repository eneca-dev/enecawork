from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_router
import logging
import sys

# Настройка логирования с выводом в консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Создаем тестовый лог, чтобы проверить работу логирования
logger = logging.getLogger(__name__)
logger.info("Application starting...")

app = FastAPI(
    title='Backend for eneca.work'
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Подключаем роутеры
app.include_router(auth_router, prefix='/auth', tags=['auth'])
# app.include_router(users_router, prefix='/users', tags=['users'])

# Здоровье сервера
@app.get('/')
async def health_check():
    return {'status': 'healthy'} 