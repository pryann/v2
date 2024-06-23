from fastapi import FastAPI
from src.modules.user import router as user_router
from src.modules.auth import router as auth_router
from src.config import get_settings
from src.utils import logger

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(user_router.router)
app.include_router(auth_router.router)
logger.info("App started")

# register_middlewares(app)
# register_exception_handlers(app)