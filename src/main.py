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
register_middlewares(app)
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn_settings_dict = {
        "app": "src.main:app",
        "host": settings.SERVER_HOST,
        "port": settings.SERVER_PORT,
        "log_level": settings.SERVER_LOG_LEVEL,
        "timeout_keep_alive": settings.SERVER_TTL,
        "reload": True if settings.APP_ENV == "dev" else False,
    }
    if settings.APP_ENV == "prod":
        uvicorn_settings_dict.update({"ssl_keyfile": "/path/to/sslkeyfile", "ssl_certfile": "/path/to/sslcertfile"})

    uvicorn.run(**uvicorn_settings_dict)
