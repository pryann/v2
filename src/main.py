from fastapi import FastAPI
from h11 import Request, Response
from src.user import router as user_router

# from .billing_address import router as billing_address_router
from src.billing_address.models import BillingAddress
from src.user.models import User
from src.database import SessionLocal, Base, engine

# table_definitions = [
#     BillingAddress.__table__,
#     User.__table__
# ]
# Base.metadata.create_all(engine, tables=table_definitions)

app = FastAPI()
app.include_router(user_router.router)
# app.include_router(billing_address_router.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
