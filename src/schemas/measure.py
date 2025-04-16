# -*- coding: utf-8 -*-

from pydantic import BaseModel

from src.schemas.parameter import ParameterId


class MeasureData(BaseModel):
    measure_date: int
    value: float | int
    parameter_id: ParameterId
