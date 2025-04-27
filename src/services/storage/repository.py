# -*- coding: utf-8 -*-


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.alert import AlertData
from src.schemas.measure import MeasureData
from src.services.storage.core.models.db_model import (
    Measures,
    Parameter,
    ParameterType,
    TypeAlert,
    WeatherStation,
    Alert,
)


class PostgresRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_parameter(self, station_id: int) -> list[dict[str, int | str]]:
        statement = (
            select(
                Parameter.id,
                ParameterType.detect_type,
                ParameterType.factor,
                ParameterType.offset,
            )
            .join(ParameterType, Parameter.parameter_type_id == ParameterType.id)
            .where(Parameter.station_id == station_id, ParameterType.is_active)
        )
        result = await self._session.execute(statement)
        parameters = result.all()
        return [parameter._asdict() for parameter in parameters]

    async def get_station_by_uid(self, uid: str) -> WeatherStation | None:
        statement = select(WeatherStation).where(
            WeatherStation.uid == uid, WeatherStation.is_active
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_alert_type_by_parameter_id(
        self, parameter_id: int
    ) -> list[TypeAlert]:
        statement = select(TypeAlert).where(
            TypeAlert.is_active, TypeAlert.parameter_id == parameter_id
        )
        result = await self._session.execute(statement)
        return result.scalars()

    async def create_measure(self, measure: MeasureData) -> Measures:
        new_measure = Measures(**measure.model_dump())
        self._session.add(new_measure)
        await self._session.flush()
        await self._session.commit()
        return new_measure

    async def create_alert(self, alert: AlertData) -> None:
        new_alert = Alert(**alert.model_dump())
        self._session.add(new_alert)
        await self._session.flush()
        await self._session.commit()