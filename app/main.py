from fastapi import FastAPI
from app.user import router as user_router
from app.auth import router as auth_router
import uvicorn
from app.config import get_settings
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version="0.1")
app.include_router(user_router.router)
# app.include_router(auth_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "app.main":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.SERVER_LOG_LEVEL,
    )
