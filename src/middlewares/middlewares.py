import os
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from src.config import get_settings
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


def setup_cors_middleware(app: FastAPI):
    cors_config = {
        "allow_origins": settings.CORS_ORIGINS_LIST,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
    # use class
    app.add_middleware(CORSMiddleware, **cors_config)


def setup_security_headers_middleware(app: FastAPI):
    # use function
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        security_headers = {
            "Content-Security-Policy": "default-src 'self'",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "same-origin",
            "X-XSS-Protection": "1; mode=block",
        }
        response.headers.update(security_headers)
        return response


def setup_process_time_middleware(app: FastAPI):
    @app.middleware("http")
    async def process_time_log_middleware(request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = str(round(time.time() - start_time, 3))
        response.headers["X-Process-Time"] = process_time
        logger.info("ProcessTime=%s", process_time)
        return response


def register_middlewares(app: FastAPI):
    setup_cors_middleware(app)
    setup_security_headers_middleware(app)
    setup_process_time_middleware(app)
    app.add_middleware(GZipMiddleware)
