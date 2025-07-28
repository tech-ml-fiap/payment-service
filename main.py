from fastapi import FastAPI
from app.adapters.driver.controllers.payment_controller import (
    router as payment_controller,
)
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


def create_app() -> FastAPI:
    app = FastAPI(title="Payment-Service")
    app.include_router(payment_controller, prefix="/api/payment", tags=["payment"])
    return app


app = create_app()
