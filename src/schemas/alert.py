# -*- coding: utf-8 -*-

from pydantic import BaseModel


class AlertData(BaseModel):
    measure_id: int
    type_alert_id: int
    create_date: int
