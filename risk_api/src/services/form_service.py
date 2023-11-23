"""Модуль сервиса для скоринга по инн."""

from functools import lru_cache
from http import HTTPStatus
from typing import Any

import httpx
from core.config import settings
from db.abstract import AbstractDB, get_db
from fastapi import Depends, HTTPException


class RiskService:
    """Сервис для поиска информацию по ИНН."""

    def __init__(self, db: AbstractDB) -> None:
        """Конструктор класса."""
        self.db = db

    async def make_request(self, inn: int) -> dict[str, Any] | list[None]:  # type: ignore[no-any-return]
        """Запрашивает информацию по ИНН."""
        url = f'https://damia.ru/api-scoring/score?inn={inn}&model=_bankrots2016&key={settings.api_key}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            status_code = response.status_code

        if status_code != HTTPStatus.OK:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Something was broke')
        return response.json()  # type: ignore[no-any-return]

    async def save_risk_data(self, document: dict[str, Any]) -> dict[str, Any] | None:
        """Записывает информацию в бд."""
        if existing_doc := await self.db.find_one('scoring', {'ИНН': document['ИНН']}):
            del existing_doc['_id']
            return existing_doc  # type: ignore[no-any-return]
        await self.db.save('scoring', document)
        return None

    async def get_risk_info(self, payload: dict[str, Any]) -> dict[str, Any] | list[None]:
        """Подготавливает документ для записи в бд."""
        if isinstance(payload, dict):
            for _id, data_by_id in payload.items():
                data_to_insert: dict[str, Any] = {}
                for key, value in data_by_id.items():
                    data_to_insert[key] = {}
                    if isinstance(value, dict):
                        for year, year_data in value.items():
                            data_to_insert[key][year] = year_data

            document = {'ИНН': _id, **data_to_insert}
            if doc := await self.save_risk_data(document):
                return doc
            del document['_id']
            return document
        return payload

    async def get_info(self, inn: int) -> dict[str, Any] | list[None]:
        """Получает информацию по инн."""
        payload = await self.make_request(inn)
        return await self.get_risk_info(payload)  # type: ignore[arg-type]


@lru_cache
def get_risk_service(
    db: AbstractDB = Depends(get_db),
) -> RiskService:
    """DI получения сервиса для FastAPI."""
    return RiskService(db)
