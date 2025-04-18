# -*- coding: utf-8 -*-
from pydantic import BaseModel


class ParameterTypeId(BaseModel):
    id: int


class DataPoint(BaseModel):
    create_date: int
    value: float


class DetectedTypeItem(BaseModel):
    type: str
    data: list[DataPoint]


class Payload(BaseModel):
    uid: int
    detected_type: list[DetectedTypeItem]
