# -*- coding: utf-8 -*-

from pydantic import BaseModel


class ParameterId(BaseModel):
    id: int
