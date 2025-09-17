from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time

# Configure Loguru logger
logger.remove()
logger.add(
    "logs/app.log",
    rotation = "500 MB",
    level = "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    backtrace = True,
    diagnose = True
)

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method

        # Tracking start time
        # logs have request params, datetime of request and duration

        # recording start time
        start_time = time.time()

        # log request details
        logger.info(
            "Incoming request",
            extra = {
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
            },
        )

        # process request and get response
        response = await call_next(request)

        # calculate the duration
        duration = time.time() - start_time

        # log response details
        logger.info(
            "Outgoing response",
            extra = {
                "status_code": response.status_code,
                "duration_sec": duration,
                "headers": dict(response.headers)
            },
        )

        return response
