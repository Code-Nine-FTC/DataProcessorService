# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.measure import MeasureData
from src.services.storage.core.models.db_model import (
    Measures,
    Parameter,
    ParameterType,
    WeatherStation,
)


class PostgresStorage:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def execute(self, datas: list[dict[str, Any]]) -> None:
        try:
            for data in datas:
                await self._process_data(data)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def _process_data(self, data: dict[str, Any]) -> None:
        station = await self._get_station_by_uid(data.get("uid"))  # type: ignore[arg-type]
        if not station:
            print("Station not found with uid:", data.get("uid"))
            return
        parameters = await self._get_all_parameter(station.id)
        if not parameters:
            print("No parameters found for station:", station.id)
            return

        for parameter in parameters:
            await self._process_parameter(data, parameter)

    async def _process_parameter(
        self, data: dict[str, Any], parameter: dict[str, Any]
    ) -> None:
        detect_type = parameter.get("detect_type")
        if detect_type not in data:
            return

        parameter_id = parameter.get("id")
        value = data.get(detect_type)
        unixtime = data.get("unixtime")

        measure = self._build_measure(
            parameter_id,  # type: ignore[arg-type]
            unixtime,  # type: ignore[arg-type]
            value,  # type: ignore[arg-type]
            offset=parameter.get("offset"),
            factor=parameter.get("factor"),
        )
        await self._create_measure(measure)

    async def _create_measure(self, measure: MeasureData) -> None:
        new_measure = Measures(**measure.model_dump())
        self._session.add(new_measure)
        await self._session.flush()

    async def _get_station_by_uid(self, uid: str) -> WeatherStation | None:
        statement = select(WeatherStation).where(
            WeatherStation.uid == uid, WeatherStation.is_active
        )
        result = await self._session.execute(statement)
        station = result.scalars().first()
        return station if station else None

    async def _get_all_parameter(
        self, station_id: int
    ) -> list[dict[str, int | str]]:
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

    @staticmethod
    def _build_measure(
        parameter_id: int,
        create_date: int,
        value: float,
        offset: float | None = None,
        factor: float | None = None,
    ) -> MeasureData:
        if factor is not None and factor != 0:
            value *= factor
        if offset is not None:
            value += offset
        return MeasureData(
            measure_date=create_date,
            value=value,
            parameter_id=parameter_id,
        )
