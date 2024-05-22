from fastapi import HTTPException


async def global_exception_handler(request, exc):
    return HTTPException(status_code=500, detail="Something went wrong")


async def http_exception_handler(request, exc):
    return exc
