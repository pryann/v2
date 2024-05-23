from fastapi import HTTPException, Request
from datetime import datetime


async def http_exception_handler(request, exc):
    timestamp = datetime.now(datetime.UTC).isoformat()
    return {"timestamp": timestamp, "path": request.url.path, "detail": exc.detail}


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    timestamp = datetime.now(datetime.UTC).isoformat()
    return {
        "timestamp": timestamp,
        "path": request.url.path,
        "detail": "Internal server error",
    }
