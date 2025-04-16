# -*- coding: utf-8 -*-

from pydantic import BaseModel

from src.schemas.parameter_type import ParameterType


class StationData(BaseModel):
    uid: str
    parameter_type: list[ParameterType]
    create_date: int


class StationId(BaseModel):
    id: int
