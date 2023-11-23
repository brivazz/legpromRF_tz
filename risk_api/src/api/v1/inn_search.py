"""API для получения информации о скоринге по инн."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from models.errors import InnError
from services.form_service import RiskService, get_risk_service

form_router = APIRouter()


@form_router.get(
    '/{inn}',
    summary='Поиск информации по ИНН',
    description='Обогащение данных о рисках по ИНН',
    response_description='Вся возможная информация о рисках компании при помощи сервиса https://damia.ru/apiscoring',
    tags=['Поиск информации по ИНН'],
    status_code=status.HTTP_200_OK,
)
async def inn_info(
    inn: int,
    service: RiskService = Depends(get_risk_service),
) -> dict[str, Any] | list[None]:
    """Получить информацию."""
    try:
        if info := await service.get_info(inn):
            return info  # type: ignore[no-any-return]
        return []
    except InnError as err:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))  # type: ignore[no-any-return]
