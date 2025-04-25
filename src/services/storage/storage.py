# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.storage.business_logic import BusinessLogic
from src.services.storage.repository import PostgresRepository


class PostgresStorage:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._data_repository = PostgresRepository(self._session)
        self._business_logic = BusinessLogic()

    async def execute(self, datas: list[dict[str, Any]]) -> None:
        try:
            for data in datas:
                await self._process_data(data)
        except Exception as e:
            await self._session.rollback()
            raise e

    async def _process_data(self, data: dict[str, Any]) -> None:
        station = await self._data_repository.get_station_by_uid(data.get("uid"))  # type: ignore[arg-type]
        if not station:
            print("Station not found with uid:", data.get("uid"))
            return
        parameters = await self._data_repository.get_all_parameter(station.id)
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

        measure = await self._data_repository.create_measure(
            self._business_logic.build_measure(
                parameter_id,  # type: ignore[arg-type]
                unixtime,  # type: ignore[arg-type]
                value,  # type: ignore[arg-type]
                offset=parameter.get("offset"),
                factor=parameter.get("factor"),
            )
        )

        type_alert = await self._data_repository.get_alert_type_by_parameter_id(
            parameter_id  # type: ignore[arg-type]
        )
        if type_alert and self._business_logic.verify_alert(measure, type_alert):
            await self._data_repository.create_alert(
                self._business_logic.build_alert(
                    measure_id=measure.id,
                    type_alert_id=type_alert.id,
                    create_date=measure.measure_date,
                )
            )
