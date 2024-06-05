from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging


def generate_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"code": status_code, "msg": message}),
    )


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(500)
    async def internal_exception_handler(request: Request, exc: Exception):
        logging.error(f"Server error occured: {exc}")
        return generate_response(500, "Internal Server Error")

    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: Exception):
        logging.error(f"Client error occured: {exc}")
        return generate_response(404, "Resource Not Found")
