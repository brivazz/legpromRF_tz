"""Описание интерфейса для работы с БД."""

import abc
from typing import Any


class AbstractDB(abc.ABC):
    """Абстрактный класс для работы с БД."""

    @abc.abstractmethod
    async def get_collection(self, collection_name: str) -> Any:
        """Получить коллекцию по названию."""

    @abc.abstractmethod
    async def save(self, collection_name: str, document: dict[str, Any]) -> str | None:
        """Создание документа в коллекции."""

    @abc.abstractmethod
    async def find_one(self, collection_name: str, query: dict[str, Any]) -> dict[str, Any] | None:
        """Выборка одного документа из БД."""


db: AbstractDB | None = None


def get_db() -> AbstractDB | None:
    """DI для FastAPI. Получаем DB."""
    return db
