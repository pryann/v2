from fastapi import Request
from app.database import SessionLocal


async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
