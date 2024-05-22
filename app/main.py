from fastapi import FastAPI
from h11 import Request
from app.user import router as user_router
import uvicorn
from app.database import SessionLocal
from app.config import get_settings


app = FastAPI()
app.include_router(user_router.router)

settings = get_settings()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


if __name__ == "app.main":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.SERVER_LOG_LEVEL,
    )
