from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(500)
    async def internal_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({"code": 500, "msg": "Internal Server Error"}),
        )
