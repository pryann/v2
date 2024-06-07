from fastapi import FastAPI
import uvicorn
from src.modules.user import router as user_router
from src.modules.auth import router as auth_router
from src.config import get_settings
from src.exceptions.exception_handlers import register_exception_handlers
from src.middlewares.middlewares import register_middlewares

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(user_router.router)
app.include_router(auth_router.router)
# register_middlewares(app)
# register_exception_handlers(app)
    