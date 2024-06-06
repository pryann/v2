from fastapi import FastAPI
from .modules.user import router as user_router
from .modules.auth import router as auth_router
from .config import get_settings
from .exceptions.exception_handlers import register_exception_handlers
from .middlewares.middlewares import register_middlewares
import uvicorn

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(user_router.router)
# app.include_router(auth_router.router)
register_middlewares(app)
register_exception_handlers(app)

def start():
    uvicorn.run(
        "src.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        reload_exclude=["__pycache__", "**/__pycache__/**"]
    )

if __name__ == "__main__":
    start()