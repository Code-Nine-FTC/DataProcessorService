# -*- coding: utf-8 -*-
from typing import Any, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.utils.common import Singleton


class ScheduleConfig(metaclass=Singleton):
    def __init__(self) -> None:
        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.configure(timezone="UTC")
        self.__scheduler.start()

    def add_job(
        self, func: Callable[[], Any], interval: int, job_id: str | None = None
    ) -> None:
        self.__scheduler.add_job(
            func,
            trigger="interval",
            seconds=interval,
            id=job_id,
            replace_existing=True,
        )
        print(f"Job {job_id} added with interval {interval} seconds.")

    def start(self) -> None:
        self.__scheduler.start()

    def stop(self) -> None:
        self.__scheduler.shutdown()
