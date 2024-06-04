from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.user import router as user_router
from src.auth import router as auth_router
from src.config import get_settings
from src.exception_handlers import register_exception_handlers
from src.middlewares import register_middlewares

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version="0.1")
app.include_router(user_router.router)
app.include_router(auth_router.router)
register_middlewares(app)
register_exception_handlers(app)
