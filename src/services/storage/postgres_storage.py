# -*- coding: utf-8 -*-
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.measure import MeasureData
from src.schemas.parameter import ParameterId
from src.schemas.parameter_type import ParameterType, ParameterTypeId
from src.schemas.station import StationData, StationId
from src.services.storage.core.models.db_model import (
    Measures,
    Parameter,
    ParameterType,
    WeatherStation,
)


class PostgresStorage:
    def __init__(
        self, session: AsyncSession, station_data: list[StationData]
    ) -> None:
        self._session = session
        self._station_data = station_data

    async def execute(self) -> None:
        try:
            for station_data in self._station_data:
                station_id = self._get_station(station_data.uid)
                parameter_type_id = self._get_parameter_type(
                    station_data.parameter_type
                )
                if not station_id or not parameter_type_id:
                    return
                parameter_id = self._get_parameter(
                    pt_id=parameter_type_id, station_id=station_id
                )
                if not parameter_id:
                    return
                await self._create_measure(
                    self._build_measure(station_data, parameter_id)
                )
                await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e

    async def get_active_detect_types(session):
        query = select(ParameterType.detect_type).where(
            ParameterType.is_active == True
        )
        result = await session.execute(query)
        return [row[0] for row in result.all()]

    async def _get_parameter_type(
        self, parameter_types: list[ParameterType]
    ) -> None | ParameterTypeId:
        query = select(ParameterType.id).where(
            ParameterType.detect_type.in_(parameter_types),
            ParameterType.is_active
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def _get_station(self, uid: int) -> None | StationId:
        query = select(WeatherStation.id).where(
            WeatherStation.uid == uid, WeatherStation.is_active == True
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def _get_parameter(
        self, pt_id: int, station_id: int
    ) -> None | ParameterId:
        query = select(Parameter.id).where(
            Parameter.parameter_type_id == pt_id,
            Parameter.weather_station_id == station_id,
            Parameter.is_active
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def _create_measure(self, measure: MeasureData) -> None:
        new_measure = Measures(measure.model_dump())
        self._session.add(new_measure)
        await self._session.flush()

    def _build_measure(
        self, station_data: StationData, parameter_id: int
    ) -> MeasureData:
        # fazer o calculo da medida!!!
        return MeasureData(
            measure_date=station_data.create_date,
            value=station_data.value,
            parameter_id=parameter_id,
        )
