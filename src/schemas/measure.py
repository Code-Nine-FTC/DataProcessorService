# -*- coding: utf-8 -*-

from pydantic import BaseModel


class MeasureData(BaseModel):
    measure_date: int
    value: float | int
    parameter_id: int
