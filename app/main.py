from fastapi import FastAPI, HTTPException
from app.user import router as user_router
import uvicorn
from app.config import get_settings
from app.middlewares import db_session_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import global_exception_handler, http_exception_handler
from fastapi.openapi.utils import get_openapi

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version="0.1")
app.include_router(user_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(db_session_middleware)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

if __name__ == "app.main":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.SERVER_LOG_LEVEL,
    )
