# -*- coding: utf-8 -*-
from src.schemas.alert import AlertData
from src.schemas.measure import MeasureData
from src.services.storage.core.models.db_model import (
    Measures,
    TypeAlert,
)
import logging

class BusinessLogic:
    @staticmethod
    def verify_alert(measure: Measures, type_alert: TypeAlert) -> bool:
        signal = type_alert.math_signal

        if signal == ">":
            op = lambda x, y: x > y  # noqa E731
        elif signal == "<":
            op = lambda x, y: x < y  # noqa E731
        elif signal == "==":
            op = lambda x, y: x == y  # noqa E731
        elif signal == ">=":
            op = lambda x, y: x >= y  # noqa E731
        elif signal == "<=":
            op = lambda x, y: x <= y  # noqa E731
        else:
            logging.warning("Invalid signal:", signal)
            return False

        return op(measure.value, type_alert.value)  # type: ignore[no-any-return, no-untyped-call]

    @staticmethod
    def build_alert(
        measure_id: int, type_alert_id: int, create_date: int
    ) -> AlertData:
        return AlertData(
            measure_id=measure_id,
            type_alert_id=type_alert_id,
            create_date=create_date,
        )

    @staticmethod
    def build_measure(
        parameter_id: int,
        create_date: int,
        value: float,
        offset: float | None = None,
        factor: float | None = None,
    ) -> MeasureData:
        if factor is not None and factor != float(0.00):
            value *= factor
        if offset is not None:
            value += offset
        return MeasureData(
            measure_date=create_date,
            value=value,
            parameter_id=parameter_id,
        )
