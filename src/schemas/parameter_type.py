# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ParameterTypeId(BaseModel):
    id: int


class ParameterType(BaseModel):
    detect_type: str
    value: float | int
