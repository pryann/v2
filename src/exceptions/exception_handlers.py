from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.exceptions.custom_exceptions import NotFoundError, AlreadyExistsError, AuthenticationError, AuthorizationError
import logging
import asyncio


def generate_response(status_code: int, message: str):
    if status_code == 500:
        message = "Internal server error"
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"status_code": status_code, "detail": message}),
    )


# def register_exception_handlers(app: FastAPI):

#     @app.exception_handler(NotFoundError)
#     async def not_found_exception_handler(request, exc):
#         return generate_response(404, str(exc))

#     @app.exception_handler(AlreadyExistsError)
#     async def already_exists_exception_handler(request, exc):
#         return generate_response(409, str(exc))

#     @app.exception_handler(AuthencticationError)
#     async def authentication_exception_handler(rrequest, exc):
#         return generate_response(401, str(exc))

#     @app.exception_handler(AuthorizationError)
#     async def authorization_exception_handler(request, exc):
#         return generate_response(403, str(exc))

#     @app.exception_handler(500)
#     def internal_server_error_handler(request, exc):
#         return generate_response(500, "Internal server error")


def register_exception_handlers(app: FastAPI):
    exceptions = {
        NotFoundError: 404,
        AlreadyExistsError: 409,
        AuthenticationError: 401,
        AuthorizationError: 403,
        asyncio.TimeoutError: 408,
        500: 500,
    }

    for exception, status_code in exceptions.items():

        @app.exception_handler(exception)
        async def exception_handler(request, exc):
            return generate_response(status_code, str(exc))
