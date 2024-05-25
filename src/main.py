from fastapi import FastAPI
from src.user import router as user_router
from src.auth import router as auth_router
import uvicorn
from src.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.exceptions import register_exception_handlers
from src.middlewares import register_middlewares

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version="0.1")
app.include_router(user_router.router)
app.include_router(auth_router.router)
register_middlewares(app)
register_exception_handlers(app)


# if __name__ == "src.main":
#     uvicorn.run(
#         "src.main:app",
#         host=settings.SERVER_HOST,
#         port=settings.SERVER_PORT,
#         log_level=settings.SERVER_LOG_LEVEL,
#         reload_dirs="src",
#         reload=True,
#     )
