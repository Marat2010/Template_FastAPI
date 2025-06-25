import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings

logger = logging.getLogger(settings.log.LOGGER_NAME)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"Response: {response.status_code} (Time: {process_time:.2f}ms) "
                f"for {request.method} {request.url.path}"
            )
            return response
        except Exception as e:
            logger.exception(f"Request failed: {str(e)}")
            raise

