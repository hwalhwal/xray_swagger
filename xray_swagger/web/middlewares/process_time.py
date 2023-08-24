from __future__ import annotations

import time
import typing

from fastapi import FastAPI
from loguru import logger

if typing.TYPE_CHECKING:
    from fastapi import Request


def register_process_time_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        Middleware to measure processing time for an api request.
        `X-Process-Time` indicates time elapsed for the request will be added to every response header
        :param request:
        :param call_next:
        :return:
        """
        url_path = request.url.path
        if url_path.startswith("/api") and not url_path.endswith(".json"):
            start_time = time.monotonic()
            response = await call_next(request)
            process_time = time.monotonic() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"Request processing time elapsed: {process_time}s")
        else:
            response = await call_next(request)
        return response
