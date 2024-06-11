# src/middleware.py

import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.config import get_settings
from src.utils.logger import get_logger

settings = (get_settings()
logger = get_logger(__name__)
global_limiter = Limiter(key_func=lambda request: request.client.host, default_limits=["100/minute"])


def setup_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_security_headers_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers.update(
            {
                "Content-Security-Policy": "default-src 'self'",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Referrer-Policy": "same-origin",
                "X-XSS-Protection": "1; mode=block",
            }
        )
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


def setup_rate_limit_middleware(app: FastAPI):
    app.state.limiter = global_limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


def register_middlewares(app: FastAPI):
    # functions
    setup_cors_middleware(app)
    setup_security_headers_middleware(app)
    setup_process_time_middleware(app)
    setup_rate_limit_middleware(app)
    # classes
    app.add_middleware(GZipMiddleware)
