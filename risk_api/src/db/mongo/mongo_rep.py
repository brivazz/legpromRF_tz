"""Реализация AbstractDB для MongoDB."""

from typing import Any

from core.config import settings
from db.abstract import AbstractDB
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection, InsertOneResult
from pymongo.errors import DuplicateKeyError


class MongoDB(AbstractDB):  # type: ignore
    """Реализация AbstractDB для взаимодействия с коллекциями MongoDB."""

    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        """Конструктор класса."""
        self._mongo_client: AsyncIOMotorClient = db_client
        self.database = self._mongo_client[settings.mongo_db]

    async def get_collection(self, collection_name: str) -> Collection:
        """Получить коллекцию по названию."""
        return self.database[collection_name]

    async def save(self, collection_name: str, document: dict[str, Any]) -> InsertOneResult | None:
        """Создание документа в коллекции."""
        collection = await self.get_collection(collection_name)
        try:
            result: InsertOneResult = await collection.insert_one(document)
            return result.inserted_id
        except DuplicateKeyError as err:
            logger.info(err)
        return None

    async def find_one(self, collection_name: str, query: str) -> dict[str, Any] | None:
        """Выборка одного документа из БД."""
        collection = await self.get_collection(collection_name)
        return await collection.find_one(query)  # type: ignore[no-any-return]
