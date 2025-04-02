# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

from src.config.lifespan import lifespan


def get_application() -> FastAPI:
    return FastAPI(
        docs_url=None,
        lifespan=lifespan,
    )


app = get_application()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=5000,
        log_level="info",
        reload=True,
    )
