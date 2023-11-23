"""Модуль создания подключения/отключения к MongoDB и создание коллекций."""

from core.config import settings
from db import abstract
from db.mongo import mongo_rep
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from pymongo.collection import Collection
from pymongo.database import Database

mongo_client: AsyncIOMotorClient | None = None


async def on_startup(mongo_uri: str) -> None:
    """Выполняет необходимые операции при запуске приложения."""
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(
            mongo_uri,
        )
        db: Database = mongo_client[settings.mongo_db]

        if 'scoring' not in await db.list_collection_names():
            collection: Collection = db['scoring']
            collection.create_index([('inn', 1)], unique=True)

        abstract.db = mongo_rep.MongoDB(mongo_client)
        logger.info('Connected to MongoDB successfully.')

    except errors.ServerSelectionTimeoutError as er:
        logger.exception(f'Error connecting to MongoDB: {er}')
    except Exception as er:
        logger.exception(f'Error connecting to MongoDB: {er}')


async def on_shutdown() -> None:
    """
    Выполняет необходимые операции при завершении работы приложения.

    Закрывает соединение с MongoDB, если оно было установлено.
    """
    if mongo_client:
        mongo_client.close()
        logger.info('Disconnected from MongoDB.')
