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
    def __init__(self, session: AsyncSession, station_data: dict[str, Any]) -> None:
        self._session = session
        self._station_data = station_data

    async def execute(self) -> None:
        try:
            station = await self._get_station_by_uid()
            if not station:
                print("Station not found with uid:", self._station_data.get("uid"))
            parameters = await self._get_all_parameter(station.id)
            for parameter in parameters:
                if parameter in self._station_data.keys():
                    parameter_id = parameter.get("id")
                    await self._create_measure(
                        self._build_measure(
                            parameter_id,
                            self._station_data.get("unixtime"),
                            self._station_data.get(parameter.get("detect_type")),
                            offset=parameter.get("offset"),
                            factor=parameter.get("factor"),
                        )
                    )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def _create_measure(self, measure: MeasureData) -> None:
        new_measure = Measures(measure.model_dump())
        self._session.add(new_measure)
        await self._session.flush()

    async def _get_station_by_uid(self) -> WeatherStation | None:
        statement = select(WeatherStation).where(
            WeatherStation.uid == self._station_data.get("uid")
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
            .where(Parameter.station_id == station_id, Parameter.is_active)
        )
        result = await self._session.execute(statement)
        parameters = result.all()
        return [parameter._asdict() for parameter in parameters]

    def _build_measure(
        self,
        parameter_id: int,
        create_date: int,
        value: float,
        offset: float | None = None,
        factor: float | None = None,
    ) -> MeasureData:
        # fazer o calculo da medida!!!
        # value = value * parameter_type.factor + parameter_type.offset??? sera que é isso mesmo???
        return MeasureData(
            measure_date=create_date,
            value=value,
            parameter_id=parameter_id,
        )
